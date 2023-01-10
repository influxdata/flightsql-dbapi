import re

from typing import Any, List, Tuple, Dict
from pyarrow import flight
from sqlalchemy import pool
from sqlalchemy.engine import reflection, default, URL
from sqlalchemy.sql import compiler
from sqlalchemy import types
from sqlalchemy.dialects import registry

from flightsql.flight import create_client

def client_from_url(url: URL) -> Tuple[flight.FlightClient, flight.FlightCallOptions]:
    fields = url.translate_connect_args(username='user')

    metadata = {k.lower(): v for k, v in url.query.items()}
    insecure = bool(metadata.pop('insecure', None))
    disable_server_verification = bool(metadata.pop('disable_server_verification', None))
    token = metadata.pop('token', None)

    return create_client(
        host=fields['host'],
        port=fields['port'],
        user=fields.pop('user', None),
        password=fields.pop('password', None),
        token=token,
        insecure=insecure,
        disable_server_verification=disable_server_verification,
        metadata=metadata,
    )

class FlightSQLDialect(default.DefaultDialect):
    """
    Establishes baseline behavior of a FlightSQL Dialect. All other
    Dialects extend from this base class.
    """

    driver = "flightsql"

    @classmethod
    def dbapi(cls):
        import flightsql as dbapi
        return dbapi

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_info: Dict[int, Any] = {}

    def connect(self, *args, **kwargs):
        return self.dbapi.connect(*args, **kwargs)

    def initialize(self, connection):
        self.sql_info = connection.connection.flightsql_get_sql_info()

    def create_connect_args(self, url: str) -> List:
        client, call_options = client_from_url(url)
        return [[client, call_options], {}]

    def get_columns(self, connection, table, schema=None, **kwargs):
        return (connection.connection.flightsql_get_columns(table, schema))

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kwargs):
        return connection.connection.flightsql_get_table_names(schema)

    @reflection.cache
    def get_schema_names(self, connection, **kwargs):
        return connection.connection.flightsql_get_schema_names()

    def get_indexes(self, connection, table_name, schema, **kwargs):
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kwargs):
        return []

    def get_foreign_keys(self, connection, table_name, schema=None, **kwargs):
        return []

    def get_view_names(self, connection, schema=None, **kwargs):
        return []

class DataFusionCompiler(compiler.SQLCompiler):
    # Force bind parameters to be replaced by their underlying value. IOx
    # doesn't support prepared statements so we'll need to do perform literal
    # binding of the parameters. This should *not* be considered safe.
    # TODO: Remove this when we're able to support prepared statements.
    def visit_bindparam(self, bindparam, within_columns_clause=False, literal_binds=False, **kwargs):
        return super().visit_bindparam(bindparam, within_columns_clause, True, **kwargs)

class DataFusionDialect(FlightSQLDialect):
    """
    DataFusionDialect is a SQLAlchemy Dialect that uses Flight SQL as its
    transport layer and for metadata lookups.

    This Dialect is currently using `information_schema` via ad-hoc queries to answer
    metadata questions. In this state DataFusionDialect is only useful against SQL
    engine's that support `infromation_schema`. This behavior will be swapped
    out for correct Flight SQL metadata calls when we have them working (see TODOs).
    """

    name = "datafusion"

    paramstyle = 'qmark'
    poolclass = pool.SingletonThreadPool
    returns_unicode_strings = True
    supports_alter = False
    supports_default_values = False
    supports_empty_insert = False
    supports_native_boolean = True
    supports_pk_autoincrement = False
    supports_statement_cache = True
    supports_unicode_binds = True
    supports_unicode_statements = True

    statement_compiler = DataFusionCompiler

    # TODO(brett): Remove this when we're ready to remove
    # `information_schema` usage.
    def get_columns(self, connection, table, schema=None, **kwargs):
        sql = 'show columns from "{}"'.format(table)
        if schema is not None and schema != "":
            sql = 'show columns from "{}"."{}"'.format(schema, table)

        cursor = connection.execute(sql)
        result = []
        for (
            table_catalog,
            table_schema,
            table_name,
            column_name,
            data_type,
            is_nullable
        ) in cursor:
            result.append({
                "name": column_name,
                "type": resolve_sql_type(data_type.lower()),
                "default": None,
                "comment": None,
                "nullable": is_nullable == "YES"
            })

        return (result)

    # TODO(brett): Remove this when we're ready to remove
    # `information_schema` usage.
    @reflection.cache
    def get_table_names(self, connection, schema=None, **kwargs):
        sql = 'select table_name from information_schema.tables'
        if schema is not None:
            sql = f"select table_name from information_schema.tables where table_schema = '{schema}'"
        result = connection.execute(sql)
        return [r[0] for r in result]

    # TODO(brett): Remove this when we're ready to remove
    # `information_schema` usage.
    @reflection.cache
    def get_schema_names(self, connection, **kwargs):
        result = connection.execute("select distinct table_schema from information_schema.tables")
        return [r[0] for r in result]

# This dictionary maps a string representation of a type, as returned by
# DataFusion in information_schema lookups, into a SQL type.
#
# TODO(brett): Delete this when we're ready to remove
# `information_schema` usage.
arrow_type_strings = {
    'utf8': types.TEXT,
    'string': types.TEXT,
    'bool': types.BOOLEAN,
    'boolean': types.BOOLEAN,
    'binary': types.BINARY,
    'date': types.DATE,

    'float': types.FLOAT,
    'double': types.FLOAT,
    'float32': types.FLOAT,
    'float64': types.FLOAT,

    'int8': types.INTEGER,
    'int16': types.INTEGER,
    'int32': types.INTEGER,
    'int64': types.BIGINT,

    'uint8': types.INTEGER,
    'uint16': types.INTEGER,
    'uint32': types.INTEGER,
    'uint64': types.BIGINT,
}

# TODO(brett): Delete this when we're ready to remove
# `information_schema` usage.
def resolve_sql_type(t: str) -> Any:
    """
    Resolves a string representation of an Arrow data type to a SQL type.

    Simple types are easy to map as they (mostly) match __str__()
    representations of the Arrow DataType values. Complex types require
    some parsing to extract the meaningful bits for mapping.
    """

    match = re.match(r"([\w]+)(\(.*\))?", t)

    if not match:
        return types.TEXT
    coltype = match.group(1)
    args = match.group(2)

    if args is None:
        return arrow_type_strings[t]

    if coltype == "dictionary":
        args = args.strip("()").split(", ")
        return arrow_type_strings[args[1]]
    if coltype == "timestamp":
        return types.TIMESTAMP
    return arrow_type_strings[t]

registry.register("datafusion.flightsql", "flightsql.sqlalchemy", "DataFusionDialect")
