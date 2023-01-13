from typing import Iterable, Optional, List, Any, Dict, Tuple
from dataclasses import dataclass
from collections import OrderedDict

from pyarrow import flight, Table
from pyarrow.ipc import IpcReadOptions, IpcWriteOptions
from google.protobuf import any_pb2
import flightsql.flightsql_pb2 as flightsql
from flightsql.util import check_closed

@dataclass
class TableRef:
    catalog: Optional[str] = None
    db_schema: Optional[str] = None
    table: str = ""

@dataclass
class CallOptions:
    timeout: Optional[float] = None
    headers: Optional[List[Tuple[bytes, bytes]]] = None
    write_options: Optional[IpcWriteOptions] = None
    read_options: Optional[IpcReadOptions] = None

class FlightSQLClient:
    def __init__(self, *args, **kwargs):
        client, headers, features = self._create_client(*args, **kwargs)
        self.client = client
        self.headers = headers
        self.features = features
        self.closed = False

    def close(self):
        self.closed = True
        self.client.close()

    def execute(self, query: str, call_options: Optional[CallOptions] = None):
        return self._get_flight_info(flightsql.CommandStatementQuery(query=query), call_options)

    def execute_update(self, query: str, call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandStatementUpdate(query=query)
        desc = self._flight_descriptor(cmd)
        writer, reader = self._do_put(desc, call_options)
        result = reader.read()
        writer.close()

        if result is None:
            return 0
        update_result = flightsql.DoPutUpdateResult()
        update_result.ParseFromString(result.to_pybytes())
        return update_result.record_count

    def get_tables(self,
                   include_schema=False,
                   catalog: Optional[str] = None,
                   table_types: Optional[Iterable[str]] = None,
                   table_name_filter_pattern: Optional[str] = None,
                   db_schema_filter_pattern: Optional[str] = None,
                   call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandGetTables(catalog=catalog,
                                         include_schema=include_schema,
                                         table_name_filter_pattern=table_name_filter_pattern,
                                         table_types=table_types,
                                         db_schema_filter_pattern=db_schema_filter_pattern)
        return self._get_flight_info(cmd, call_options)

    def get_db_schemas(self,
                       catalog: Optional[str] = None,
                       db_schema_filter_pattern: Optional[str] = None,
                       call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandGetDbSchemas(catalog=catalog,
                                            db_schema_filter_pattern=db_schema_filter_pattern)
        return self._get_flight_info(cmd, call_options)

    def get_catalogs(self, call_options: Optional[CallOptions] = None):
        return self._get_flight_info(flightsql.CommandGetCatalogs(), call_options)

    def get_primary_keys(self, table: TableRef, call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandGetPrimaryKeys(catalog=table.catalog, db_schema=table.db_schema, table=table.table)
        return self._get_flight_info(cmd, call_options)

    def get_exported_keys(self, table: TableRef, call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandGetExportedKeys(catalog=table.catalog, db_schema=table.db_schema, table=table.table)
        return self._get_flight_info(cmd, call_options)

    def get_imported_keys(self, table: TableRef, call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandGetImportedKeys(catalog=table.catalog, db_schema=table.db_schema, table=table.table)
        return self._get_flight_info(cmd, call_options)

    def get_cross_reference(self, pk_table: TableRef, fk_table: TableRef, call_options: Optional[CallOptions] = None):
        cmd = flightsql.CommandGetCrossReference(
                fk_catalog=fk_table.catalog,
                fk_db_schema=fk_table.db_schema,
                fk_table=fk_table.table,
                pk_catalog=pk_table.catalog,
                pk_db_schema=pk_table.db_schema,
                pk_table=pk_table.table)
        return self._get_flight_info(cmd, call_options)

    def get_xdbc_type_info(self, data_type: Optional[int], call_options: Optional[CallOptions] = None):
        return self._get_flight_info(flightsql.CommandGetXdbcTypeInfo(data_type=data_type), call_options)

    def prepare(self, query: str, call_options: Optional[CallOptions] = None):
        raise NotImplementedError("prepare is not implemented")

    def get_table_types(self, call_options: Optional[CallOptions] = None):
        return self._get_flight_info(flightsql.CommandGetTableTypes(), call_options)

    def get_sql_info(self, info: List[int], call_options: Optional[CallOptions] = None):
        return self._get_flight_info(flightsql.CommandGetSqlInfo(info=info), call_options)

    @check_closed
    def do_get(self, ticket, call_options: Optional[CallOptions] = None):
        options = self._merged_call_options(call_options)
        return self.client.do_get(ticket, options)

    @check_closed
    def _do_put(self, desc, call_options: Optional[CallOptions] = None):
        options = self._merged_call_options(call_options)
        return self.client.do_put(desc, Table.from_arrays([]).schema, options)

    @check_closed
    def _get_flight_info(self, command, call_options: Optional[CallOptions] = None):
        options = self._merged_call_options(call_options)
        return self.client.get_flight_info(self._flight_descriptor(command), options)

    def _flight_descriptor(self, inner: Any) -> flight.FlightDescriptor:
        any = any_pb2.Any()
        any.Pack(inner)
        return flight.FlightDescriptor.for_command(any.SerializeToString())

    def _merged_call_options(self, call_options: Optional[CallOptions] = None):
        headers = self.headers
        timeout = None
        read_options = None
        write_options = None

        if call_options is not None:
            timeout = call_options.timeout
            read_options = call_options.read_options
            write_options = call_options.write_options

            if call_options.headers is not None:
                headers = headers + call_options.headers

            # Deduplicate entries (tuples) based on their first field. Given two
            # duplicate entries, the last one will win.
            headers = list(OrderedDict(headers).items())

        return flight.FlightCallOptions(timeout=timeout,
                                        headers=headers,
                                        read_options=read_options,
                                        write_options=write_options)

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
                                               List[Tuple[str, str]],
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

        return client, headers, features
