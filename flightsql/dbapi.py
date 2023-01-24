from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Union

import pyarrow as pa
import pyarrow.ipc as ipc
from sqlalchemy import types

from flightsql.client import FlightSQLClient, TableRef
from flightsql.exceptions import Error
from flightsql.util import check_closed

paramstyle = "qmark"
apilevel = "2.0"

ExecuteParams = Union[Tuple[Any, ...], List[Any]]


def check_result(f):
    def g(self, *args, **kwargs):
        if self._results is None:
            raise Error("called before execute")
        return f(self, *args, **kwargs)

    return g


class Cursor:
    def __init__(self, client: FlightSQLClient):
        self.client = client
        self.arraysize = 1
        self.closed = False
        self.description: Optional[List[Any]] = None
        self._results: List[Sequence[Any]] = []

    @check_closed
    def __iter__(self) -> Iterator[Sequence[Any]]:
        return iter(self._results)

    def __enter__(self) -> "Cursor":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    @check_closed
    def close(self) -> None:
        self.closed = True

    @check_closed
    def execute(self, query: str, params: Optional[ExecuteParams] = None) -> "Cursor":
        self.description = None
        self._results = []

        if params is None or len(params) == 0:
            info = self.client.execute(query)
            reader = self.client.do_get(info.endpoints[0].ticket)
            self._results, self.description = dbapi_results(reader.read_all())
            return self

        with self.client.prepare(query) as stmt:
            builder = ParameterRecordBuilder(params or ())
            record = builder.build_record()
            info = stmt.execute(record)
            reader = self.client.do_get(info.endpoints[0].ticket)
            self._results, self.description = dbapi_results(reader.read_all())
            return self

    def executemany(self, query: str, param_seq: Sequence[ExecuteParams]) -> "Cursor":
        self.description = None
        self._results = []

        if param_seq is None or len(param_seq) == 0:
            return self.execute(query)

        with self.client.prepare(query) as stmt:
            for params in param_seq:
                builder = ParameterRecordBuilder(params or ())
                record = builder.build_record()
                info = stmt.execute(record)
                self.client.do_get(info.endpoints[0].ticket).read_all()
            return self

    @check_result
    @check_closed
    def fetchone(self) -> Optional[Sequence[Any]]:
        try:
            return self._results.pop(0)
        except IndexError:
            return None

    @check_result
    @check_closed
    def fetchmany(self, size: Optional[int] = None) -> Sequence[Sequence[Any]]:
        size = size or self.arraysize
        out = self._results[:size]
        self._results = self._results[size:]
        return out

    @check_result
    @check_closed
    def fetchall(self) -> Sequence[Sequence[Any]]:
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


class Connection:
    def __init__(self, client: FlightSQLClient, **kwargs):
        self.client = client
        self.closed = False
        self.cursors: List[Cursor] = []

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, *args) -> None:
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
    def execute(self, *args, **kwargs) -> Cursor:
        cursor = self.cursor()
        return cursor.execute(*args, **kwargs)

    @check_closed
    def executemany(self, *args, **kwargs) -> Cursor:
        cursor = self.cursor()
        return cursor.executemany(*args, **kwargs)

    @check_closed
    def flightsql_get_columns(self, table_name: str, schema: Optional[str] = None) -> List[Dict]:
        """Get the columns of a table using Flight SQL."""
        info = self.client.get_tables(
            table_name_filter_pattern=table_name, db_schema_filter_pattern=schema, include_schema=True
        )
        reader = self.client.do_get(info.endpoints[0].ticket)
        table = reader.read_all()
        # TODO(brett): Accessing the first element here without caution. Fix this.
        table_schema = table.column("table_schema")[0].as_py()
        reader = ipc.open_stream(table_schema)
        return column_specs(reader.schema)

    @check_closed
    def flightsql_get_table_names(self, schema: Optional[str] = None) -> List[str]:
        """Get the names of all tables within the schema."""
        info = self.client.get_tables(db_schema_filter_pattern=schema)
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_pandas()["table_name"].tolist()

    @check_closed
    def flightsql_get_schema_names(self) -> List[str]:
        """Get the names of all schemas."""
        info = self.client.get_db_schemas()
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_pandas()["db_schema_name"].tolist()

    @check_closed
    def flightsql_get_sql_info(self, info: List[int]) -> Dict[int, Any]:
        """Get metadata about the server and its SQL features."""
        finfo = self.client.get_sql_info(info)
        reader = self.client.do_get(finfo.endpoints[0].ticket)
        values = reader.read_all().to_pylist()
        return {v["info_name"]: v["value"] for v in values}

    @check_closed
    def flightsql_get_primary_keys(self, table: str, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        ref = TableRef(table=table, db_schema=schema)
        info = self.client.get_primary_keys(ref)
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_all().to_pylist()

    @check_closed
    def flightsql_get_foreign_keys(self, table: str, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        ref = TableRef(table=table, db_schema=schema)
        info = self.client.get_imported_keys(ref)
        reader = self.client.do_get(info.endpoints[0].ticket)
        return reader.read_all().to_pylist()

    @property
    def features(self) -> Dict[str, str]:
        return self.client.features


def connect(client: FlightSQLClient, **kwargs) -> Connection:
    """Connects to a Flight SQL server."""
    return Connection(client, **kwargs)


def column_specs(schema: pa.Schema) -> List[Dict]:
    cols = []
    for i in range(0, len(schema)):
        field = schema.field(i)
        cols.append(
            {
                "name": field.name,
                "type": resolve_sql_type(field.type),
                "default": None,
                "comment": None,
                "nullable": field.nullable,
            }
        )
    return cols


def dbapi_results(table: pa.Table) -> Tuple[List, List]:
    """
    Read all chunks, convert into NumPy/Pandas and return the values and
    column descriptions. Column descriptions are derived from the original Arrow
    schema fields.
    """
    df = table.to_pandas(date_as_object=False, integer_object_nulls=True)
    descriptions = arrow_column_descriptions(table.schema)
    return df.values.tolist(), descriptions


def arrow_column_descriptions(schema: pa.Schema) -> List[Tuple[str, Any]]:
    """Map Arrow schema fields to SQL types."""
    description = []
    for i, t in enumerate(schema.types):
        description.append((schema.names[i], resolve_sql_type(t)))
    return description


def resolve_sql_type(t: pa.DataType):
    """Resolves an Arrow DataType value to a SQL type."""

    if pa.types.is_timestamp(t):
        return types.TIMESTAMP
    if pa.types.is_time(t):
        return types.TIME
    if pa.types.is_date(t):
        return types.DATE
    if pa.types.is_binary(t):
        return types.BINARY
    if pa.types.is_boolean(t):
        return types.BOOLEAN
    if pa.types.is_decimal(t):
        return types.DECIMAL
    if pa.types.is_floating(t):
        return types.FLOAT
    if pa.types.is_string(t):
        return types.TEXT

    if pa.types.is_signed_integer(t) and not pa.types.is_int64(t):
        return types.INTEGER
    if pa.types.is_int64(t):
        return types.BIGINT

    # TODO(brett): Find a way to deal with unsigned integers.
    if pa.types.is_unsigned_integer(t) and not pa.types.is_uint64(t):
        return types.INTEGER
    if pa.types.is_uint64(t):
        return types.BIGINT

    # TODO(brett): I'd like to be permissive of unknown types here, but I'm not
    # sure what type we should fall back to.
    return types.BLOB


class ParameterRecordBuilder:
    """
    Builds a PyArrow RecordBatch from a list of parameters for prepared statements.

    Each parameter value is packed into a UnionArray (dense) of length 1. This
    allows the upstream to accept a different type for each parameter in the
    input Tuple. These UnionArray values are then packed into a RecordBatch.
    """

    union_positions = {t: idx for idx, t in enumerate([int, float, str, bytes, bool])}
    arrow_types = {int: pa.int64, float: pa.float64, str: pa.utf8, bytes: pa.binary, bool: pa.bool_}

    def __init__(self, values: ExecuteParams):
        self.values = values

    def union_array_for_value(self, value: Any) -> pa.UnionArray:
        """Builds a PyArrow UnionArray around a value."""
        pytype = type(value)
        if pytype not in self.union_positions:
            raise Error(f'unable to map "{pytype.__name__}" type to PyArrow datatype')

        children = []
        type_id = -1
        for t, idx in self.union_positions.items():
            arrow_type = self.arrow_types[t]()
            if t == pytype:
                type_id = idx
                values = [value]
            else:
                values = []
            children.append(pa.array(values, type=arrow_type))

        return pa.UnionArray.from_dense(pa.array([type_id], type=pa.int8()), pa.array([0], type=pa.int32()), children)

    def build_record(self) -> pa.RecordBatch:
        """
        Builds a PyArrow RecordBatch containing UnionArrays for all parameters.
        """
        if len(self.values) == 0:
            return pa.RecordBatch.from_arrays([], names=[])

        columns = [self.union_array_for_value(v) for v in self.values]
        names = [f"param_{i}" for i in range(len(columns))]
        return pa.RecordBatch.from_arrays(columns, names=names)
