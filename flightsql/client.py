from typing import Iterable, Optional, List, Any, Dict, Tuple
from dataclasses import dataclass

from pyarrow import flight
from google.protobuf import any_pb2
import flightsql.flightsql_pb2 as flightsql
from flightsql.util import check_closed

@dataclass
class TableRef:
    catalog: Optional[str] = None
    db_schema: Optional[str] = None
    table: str = ""

class FlightSQLClient:
    def __init__(self, *args, **kwargs):
        client, options, features = self._create_client(*args, **kwargs)
        self.client = client
        self.options = options
        self.features = features
        self.closed = False

    def close(self):
        self.closed = True
        self.client.close()

    def execute(self, query: str):
        return self._get_flight_info(flightsql.CommandStatementQuery(query=query))

    def get_tables(self,
                   include_schema=False,
                   catalog: Optional[str] = None,
                   table_types: Optional[Iterable[str]] = None,
                   table_name_filter_pattern: Optional[str] = None,
                   db_schema_filter_pattern: Optional[str] = None):
        cmd = flightsql.CommandGetTables(catalog=catalog,
                                         include_schema=include_schema,
                                         table_name_filter_pattern=table_name_filter_pattern,
                                         table_types=table_types,
                                         db_schema_filter_pattern=db_schema_filter_pattern)
        return self._get_flight_info(cmd)

    def get_db_schemas(self,
                       catalog: Optional[str] = None,
                       db_schema_filter_pattern: Optional[str] = None):
        cmd = flightsql.CommandGetDbSchemas(catalog=catalog,
                                            db_schema_filter_pattern=db_schema_filter_pattern)
        return self._get_flight_info(cmd)

    def get_catalogs(self):
        return self._get_flight_info(flightsql.CommandGetCatalogs())

    def get_primary_keys(self, table: TableRef):
        cmd = flightsql.CommandGetPrimaryKeys(catalog=table.catalog, db_schema=table.db_schema, table=table.table)
        return self._get_flight_info(cmd)

    def get_exported_keys(self, table: TableRef):
        cmd = flightsql.CommandGetExportedKeys(catalog=table.catalog, db_schema=table.db_schema, table=table.table)
        return self._get_flight_info(cmd)

    def get_imported_keys(self, table: TableRef):
        cmd = flightsql.CommandGetImportedKeys(catalog=table.catalog, db_schema=table.db_schema, table=table.table)
        return self._get_flight_info(cmd)

    def get_cross_reference(self, pk_table: TableRef, fk_table: TableRef):
        cmd = flightsql.CommandGetCrossReference(
                fk_catalog=fk_table.catalog,
                fk_db_schema=fk_table.db_schema,
                fk_table=fk_table.table,
                pk_catalog=pk_table.catalog,
                pk_db_schema=pk_table.db_schema,
                pk_table=pk_table.table)
        return self._get_flight_info(cmd)

    def get_xdbc_type_info(self, data_type: Optional[int]):
        return self._get_flight_info(flightsql.CommandGetXdbcTypeInfo(data_type=data_type))

    def prepare(self, query: str):
        raise NotImplementedError("prepare is not implemented")

    def get_table_types(self):
        return self._get_flight_info(flightsql.CommandGetTableTypes())

    def get_sql_info(self, info: List[int]):
        return self._get_flight_info(flightsql.CommandGetSqlInfo(info=info))

    @check_closed
    def do_get(self, ticket):
        return self.client.do_get(ticket, self.options)

    @check_closed
    def _get_flight_info(self, command):
        return self.client.get_flight_info(self._flight_descriptor(command), self.options)

    def _flight_descriptor(self, inner: Any) -> flight.FlightDescriptor:
        any = any_pb2.Any()
        any.Pack(inner)
        return flight.FlightDescriptor.for_command(any.SerializeToString())

    def _create_client(self,
                       host: str = "localhost",
                       port: int = 443,
                       user: Optional[str] = None,
                       password: Optional[str] = None,
                       token: Optional[str] = None,
                       insecure: Optional[bool] = None,
                       disable_server_verification: Optional[bool] = None,
                       metadata: Optional[Dict[str, str]] = None,
                       features: Optional[Dict[str, str]] = None,
                       **kwargs: Any) -> Tuple[flight.FlightClient,
                                               flight.FlightCallOptions,
                                               Dict[str, str]]:

        protocol = 'tls'
        client_args = {}
        if insecure:
            protocol = 'tcp'
        elif disable_server_verification:
            client_args['disable_server_verification'] = True

        url = f"grpc+{protocol}://{host}:{port}"
        client = flight.FlightClient(url, **client_args)

        headers = []
        if user or password:
            headers.append(client.authenticate_basic_token(user, password))
        else:
            headers.append((b'authorization', f"Bearer {token}".encode('utf-8')))

        if metadata:
            for k, v in metadata.items():
                headers.append((k.encode('utf-8'), v.encode('utf-8')))

        if features is None:
            features = {}

        return client, flight.FlightCallOptions(headers=headers), features
