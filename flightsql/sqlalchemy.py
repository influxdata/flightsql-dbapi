from typing import Any, Dict, List

from sqlalchemy import pool
from sqlalchemy.dialects import registry
from sqlalchemy.engine import URL, default, reflection
from sqlalchemy.sql import compiler

import flightsql.flightsql_pb2 as flightsql
from flightsql.client import FlightSQLClient

feature_prefix = "feature-"

FEATURE_PREPARED_STATEMENTS = "sqlalchemy-prepared-statements"
FEATURE_PRIMARY_KEYS = "sqlalchemy-primary-keys"


def client_from_url(url: URL) -> FlightSQLClient:
    fields = url.translate_connect_args(username="user")

    metadata = {k.lower(): v for k, v in url.query.items()}
    insecure = bool(metadata.pop("insecure", None))
    disable_server_verification = bool(metadata.pop("disable_server_verification", None))
    token = metadata.pop("token", None)

    features = {}
    for k in list(metadata.keys()):
        if k.startswith(feature_prefix):
            features[k[len(feature_prefix) :]] = metadata.pop(k)

    return FlightSQLClient(
        host=fields["host"],
        port=fields["port"],
        user=fields.pop("user", None),
        password=fields.pop("password", None),
        token=token,
        insecure=insecure,
        disable_server_verification=disable_server_verification,
        metadata=metadata,
        features=features,
    )


class FlightSQLDialect(default.DefaultDialect):
    """
    Establishes baseline behavior of a FlightSQL Dialect. All other
    Dialects extend from this base class.
    """

    driver = "flightsql"
    sql_info: Dict[int, Any] = {}

    sql_info_values = [
        flightsql.FLIGHT_SQL_SERVER_NAME,
        flightsql.FLIGHT_SQL_SERVER_ARROW_VERSION,
        flightsql.FLIGHT_SQL_SERVER_READ_ONLY,
        flightsql.SQL_IDENTIFIER_QUOTE_CHAR,
    ]

    @classmethod
    def dbapi(cls):
        import flightsql as dbapi

        return dbapi

    def connect(self, *args, **kwargs):
        return self.dbapi.connect(*args, **kwargs)

    def initialize(self, connection):
        super().initialize(connection)

        self.sql_info = connection.connection.flightsql_get_sql_info(self.sql_info_values)

        # Set the quote character for identifiers.
        self.identifier_preparer.initial_quote = self.sql_info[flightsql.SQL_IDENTIFIER_QUOTE_CHAR]
        self.identifier_preparer.final_quote = self.identifier_preparer.initial_quote

        read_only = self.sql_info[flightsql.FLIGHT_SQL_SERVER_READ_ONLY]
        self.supports_delete = not read_only
        self.supports_alter = not read_only

    def create_connect_args(self, url: URL) -> List:
        client = client_from_url(url)
        return [[client], {}]

    @reflection.cache
    def get_columns(self, connection, table, schema=None, **kwargs):
        return connection.connection.flightsql_get_columns(table, schema)

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kwargs):
        return connection.connection.flightsql_get_table_names(schema)

    @reflection.cache
    def get_schema_names(self, connection, **kwargs):
        return connection.connection.flightsql_get_schema_names()

    @reflection.cache
    def has_table(self, connection, table, schema=None, **kwargs):
        return table in self.get_table_names(connection, schema)

    def get_indexes(self, connection, table_name, schema, **kwargs):
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kwargs):
        conn = connection.connection
        primary_keys_enabled = conn.features.get(FEATURE_PRIMARY_KEYS)
        if primary_keys_enabled != "on":
            return []

        columns = conn.flightsql_get_primary_keys(table_name, schema=schema)
        if len(columns) == 0:
            return {"constrained_columns": [], "name": None}
        names = [v["column_name"] for v in columns]
        return {"constrained_columns": names, "name": columns[0]["key_name"]}

    def get_foreign_keys(self, connection, table_name, schema=None, **kwargs):
        return []

    def get_view_names(self, connection, schema=None, **kwargs):
        return []


class LiteralBindCompiler(compiler.SQLCompiler):
    # Force bind parameters to be replaced by their underlying value. IOx
    # doesn't support prepared statements so we'll need to do perform literal
    # binding of the parameters. This should *not* be considered safe.
    # TODO: Remove this when we're able to support prepared statements.
    def visit_bindparam(self, bindparam, within_columns_clause=False, literal_binds=False, **kwargs):
        return super().visit_bindparam(bindparam, within_columns_clause, True, **kwargs)


class DataFusionDialect(FlightSQLDialect):
    """
    DataFusionDialect is a SQLAlchemy Dialect that uses Flight SQL as its
    transport layer and for metadata lookups. It is specifically tuned for the
    baseline configuration of a DataFusion execution engine.

    This Dialect is currently using `information_schema` via ad-hoc queries to answer
    metadata questions. In this state DataFusionDialect is only useful against SQL
    engine's that support `infromation_schema`. This behavior will be swapped
    out for correct Flight SQL metadata calls when we have them working (see TODOs).
    """

    name = "datafusion"

    paramstyle = "qmark"
    poolclass = pool.SingletonThreadPool
    returns_unicode_strings = True
    supports_default_values = False
    supports_empty_insert = False
    supports_native_boolean = True
    supports_pk_autoincrement = False
    supports_statement_cache = True
    supports_unicode_binds = True
    supports_unicode_statements = True
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False

    def initialize(self, connection):
        super().initialize(connection)

        # Use the literal binding SQL compiler if we haven't turned on the
        # prepared statements feature. This ensures that the client won't
        # attempt to create a prepared statement if the upstream server isn't
        # expected to support it.
        prepared_statements_enabled = connection.connection.features.get(FEATURE_PREPARED_STATEMENTS)
        if prepared_statements_enabled != "on":
            self.statement_compiler = LiteralBindCompiler
        else:
            self.statement_compiler = compiler.SQLCompiler


registry.register("datafusion.flightsql", "flightsql.sqlalchemy", "DataFusionDialect")
