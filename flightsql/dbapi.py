from typing import Any, Optional, Tuple, List, Dict

from pyarrow import Table, Schema
import pyarrow.ipc as ipc
from flightsql.arrow import resolve_sql_type
from flightsql.client import FlightSQLClient, TableRef
from flightsql.exceptions import Error, NotSupportedError
from flightsql.util import check_closed

paramstyle = "pyformat"
apilevel = "2.0"

def check_result(f):
    def g(self, *args, **kwargs):
        if self._results is None:
            raise Error('called before execute')
        return f(self, *args, **kwargs)
    return g

class Cursor():
    def __init__(self, client: FlightSQLClient):
        self.client = client
        self.arraysize = 1
        self.closed = False
        self.description: Optional[List[Any]] = None
        self._results: List[Any] = []

    @check_closed
    def __iter__(self):
        return iter(self._results)

    @check_closed
    def close(self) -> None:
        self.closed = True

    @check_closed
    def execute(self, query: str, params=None) -> "Cursor":
        self.description = None
        info = self.client.execute(query)
        reader = self.client.do_get(info.endpoints[0].ticket)
        self._results, self.description = dbapi_results(reader.read_all())
        return self

    @check_closed
    def executemany(self, query: str):
        raise NotSupportedError('executemany is not supported')

    @check_result
    @check_closed
    def fetchone(self) -> Optional[Tuple[Any, ...]]:
        try:
            return self._results.pop(0)
        except IndexError:
            return None

    @check_result
    @check_closed
    def fetchmany(self, size: Optional[int] = None) -> List[Tuple[Any, ...]]:
        size = size or self.arraysize
        out = self._results[:size]
        self._results = self._results[size:]
        return out

    @check_result
    @check_closed
    def fetchall(self):
        out = self._results[:]
        self._results = []
        return out

    @check_closed
    def setinputsizes(self, sizes):
        pass

    @check_closed
    def setoutputsizes(self, sizes):
        pass

    @property
    @check_result
    @check_closed
    def rowcount(self) -> int:
        return len(self._results)

class Connection():
    def __init__(self, client: FlightSQLClient, **kwargs):
        self.client = client
        self.closed = False
        self.cursors: List[Cursor] = []

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, *args) -> None:
        self.commit()
        self.close()

    @check_closed
    def commit(self):
        pass

    @check_closed
    def rollback(self):
        pass

    @check_closed
    def close(self) -> None:
        self.closed = True
        for cursor in self.cursors:
            cursor.close()

    @check_closed
    def cursor(self) -> Cursor:
        cursor = Cursor(self.client)
        self.cursors.append(cursor)
        return cursor

    @check_closed
    def execute(self, query) -> Cursor:
        cursor = self.cursor()
        return cursor.execute(query)

    @check_closed
    def flightsql_get_columns(self, table_name, schema):
        """Get the columns of a table using Flight SQL."""
        info = self.client.get_tables(table_name_filter_pattern=table_name,
                                      db_schema_filter_pattern=schema,
                                      include_schema=True)
        reader = self.client.do_get(info.endpoints[0].ticket)
        table = reader.read_all()
        # TODO(brett): Accessing the first element here without caution. Fix this.
        table_schema = table.column('table_schema')[0].as_py()
        reader = ipc.open_stream(table_schema)
        return column_specs(reader.schema)

    @check_closed
    def flightsql_get_table_names(self, schema):
        """Get the names of all tables within the schema."""
        info = self.client.get_tables(db_schema_filter_pattern=schema)
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_pandas()['table_name'].tolist()

    @check_closed
    def flightsql_get_schema_names(self):
        """Get the names of all schemas."""
        info = self.client.get_db_schemas()
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_pandas()['db_schema_name'].tolist()

    @check_closed
    def flightsql_get_sql_info(self, info: List[int]):
        """Get metadata about the server and its SQL features."""
        finfo = self.client.get_sql_info(info)
        reader = self.client.do_get(finfo.endpoints[0].ticket)
        values = reader.read_all().to_pylist()
        return {v['info_name']: v['value'] for v in values}

    @check_closed
    def flightsql_get_primary_keys(self, table: str, schema: Optional[str] = None):
        ref = TableRef(table=table, db_schema=schema)
        info = self.client.get_primary_keys(ref)
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_all().to_pylist()

    @check_closed
    def flightsql_get_foreign_keys(self, table: str, schema: Optional[str] = None):
        ref = TableRef(table=table, db_schema=schema)
        info = self.client.get_imported_keys(ref)
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_all().to_pylist()

    def features(self):
        return self.client.features

def connect(*args, **kwargs) -> Connection:
    return Connection(*args, **kwargs)

def column_specs(schema: Schema) -> List[Dict]:
    cols = []
    for i in range(0, len(schema)):
        field = schema.field(i)
        cols.append({
            "name": field.name,
            "type": resolve_sql_type(field.type),
            "default": None,
            "comment": None,
            "nullable": field.nullable,
        })
    return cols

def dbapi_results(table: Table) -> Tuple[List, List]:
    """
    Read all chunks, convert into NumPy/Pandas and return the values and
    column descriptions. Column descriptions are derived from the original Arrow
    schema fields.
    """
    df = table.to_pandas(date_as_object=False, integer_object_nulls=True)
    descriptions = arrow_column_descriptions(table.schema)
    return df.values.tolist(), descriptions

def arrow_column_descriptions(schema: Schema) -> List[Tuple[str, Any]]:
    """Map Arrow schema fields to SQL types."""
    description = []
    for i, t in enumerate(schema.types):
        description.append((schema.names[i], resolve_sql_type(t)))
    return description
