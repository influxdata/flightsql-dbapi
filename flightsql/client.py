from typing import Iterable, Optional, List, Any, Dict, Tuple

from pyarrow import flight
from google.protobuf import any_pb2
import flightsql.flightsql_pb2 as flightsql

class FlightSQLClient:
    def __init__(self, *args, **kwargs):
        client, options, features = self._create_client(*args, **kwargs)
        self.client = client
        self.options = options
        self.features = features

    def execute(self, query: str):
        return self._do_get(flightsql.CommandStatementQuery(query=query))

    def get_tables(self,
                   include_schema=False,
                   catalog: Optional[str] = None,
                   table_types: Optional[Iterable[str]] = None,
                   table_name_filter_pattern: Optional[str] = None,
                   db_schema_filter_pattern: Optional[str] = None):
        return self._do_get(flightsql.CommandGetTables(catalog=catalog,
                                                       include_schema=include_schema,
                                                       table_name_filter_pattern=table_name_filter_pattern,
                                                       table_types=table_types,
                                                       db_schema_filter_pattern=db_schema_filter_pattern))

    def get_db_schemas(self,
                       catalog: Optional[str] = None,
                       db_schema_filter_pattern: Optional[str] = None):
        return self._do_get(flightsql.CommandGetDbSchemas(catalog=catalog,
                                                          db_schema_filter_pattern=db_schema_filter_pattern))

    def get_sql_info(self, info: List[int]):
        return self._do_get(flightsql.CommandGetSqlInfo(info=info))

    def _do_get(self, command):
        info = self.client.get_flight_info(self._flight_descriptor(command), self.options)
        return self.client.do_get(info.endpoints[0].ticket, self.options)

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
