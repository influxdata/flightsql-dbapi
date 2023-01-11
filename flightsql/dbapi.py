from typing import Any, Optional, Tuple, List, Dict

from pyarrow import Table, Schema
import pyarrow.ipc as ipc
from flightsql.arrow import resolve_sql_type
from flightsql.client import FlightSQLClient
from flightsql.exceptions import Error, NotSupportedError

paramstyle = "pyformat"
apilevel = "2.0"

def check_closed(f):
    def g(self, *args, **kwargs):
        if self.closed:
            raise Error(f"{self.__class__.__name__} already closed")
        return f(self, *args, **kwargs)
    return g

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
        self._results, self.description = flightsql_execute(query, self.client)
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
    def flightsql_get_columns(self, table, schema):
        return flightsql_get_columns(table, schema, self.client)

    @check_closed
    def flightsql_get_table_names(self, schema):
        return flightsql_get_table_names(schema, self.client)

    @check_closed
    def flightsql_get_schema_names(self):
        return flightsql_get_schema_names(self.client)

    @check_closed
    def flightsql_get_sql_info(self, info: List[int]):
        return flightsql_get_sql_info(info, self.client)

    def features(self):
        return self.client.features

def connect(*args, **kwargs) -> Connection:
    return Connection(*args, **kwargs)

def flightsql_execute(query: str, client: FlightSQLClient) -> Tuple[List, List]:
    """Execute a Flight SQL query."""
    return dbapi_results(client.execute(query).read_all())

def flightsql_get_columns(table_name: str, schema: str, client: FlightSQLClient) -> List[Dict[Any, Any]]:
    """Get the columns of a table using Flight SQL."""
    reader = client.get_tables(table_name_filter_pattern=table_name,
                               db_schema_filter_pattern=schema,
                               include_schema=True)
    table = reader.read_all()
    # TODO(brett): Accessing the first element here without caution. Fix this.
    table_schema = table.column('table_schema')[0].as_py()
    reader = ipc.open_stream(table_schema)
    return column_specs(reader.schema)

def flightsql_get_table_names(schema: str, client: FlightSQLClient) -> Tuple[List, List]:
    """Get the names of all tables within the schema."""
    reader = client.get_tables(db_schema_filter_pattern=schema)
    return reader.read_pandas()['table_name'].tolist()

def flightsql_get_schema_names(client: FlightSQLClient) -> Tuple[List, List]:
    """Get the names of all schemas."""
    reader = client.get_schemas()
    return reader.read_pandas()['db_schema_name'].tolist()

def flightsql_get_sql_info(info: List[int], client: FlightSQLClient) -> Dict[int, Any]:
    """Get metadata about the server and its SQL features."""
    reader = client.get_sql_info(info)
    values = reader.read_all().to_pylist()
    return {v['info_name']: v['value'] for v in values}

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
