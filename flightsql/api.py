from typing import Any, Optional, Tuple, List, Dict

import pyarrow.ipc as ipc
from pyarrow import flight, Table, Schema
from google.protobuf import any_pb2
from flightsql.arrow import resolve_sql_type
import flightsql.flightsql_pb2 as flightsql

def flightsql_execute(query: str,
                      client: flight.FlightClient,
                      options: Optional[flight.FlightCallOptions] = None) -> Tuple[List, List]:
    """Execute a Flight SQL query."""
    command = flightsql.CommandStatementQuery(query=query)
    info = client.get_flight_info(flight_descriptor(command), options)
    reader = client.do_get(info.endpoints[0].ticket, options)
    return dbapi_results(reader.read_all())

def flightsql_get_columns(table_name: str,
                          schema: str,
                          client: flight.FlightClient,
                          options: Optional[flight.FlightCallOptions] = None) -> List[Dict[Any, Any]]:
    """Get the columns of a table using Flight SQL."""
    command = flightsql.CommandGetTables(db_schema_filter_pattern=schema,
                                         table_name_filter_pattern=table_name,
                                         include_schema=True)
    info = client.get_flight_info(flight_descriptor(command), options)
    reader = client.do_get(info.endpoints[0].ticket, options)
    table = reader.read_all()

    # TODO(brett): Accessing the first element here without caution. Fix this.
    table_schema = table.column('table_schema')[0].as_py()
    reader = ipc.open_stream(table_schema)
    return column_specs(reader.schema)

def flightsql_get_table_names(schema: str,
                              client: flight.FlightClient,
                              options: Optional[flight.FlightCallOptions] = None) -> Tuple[List, List]:
    """Get the names of all tables within the schema."""
    command = flightsql.CommandGetTables(db_schema_filter_pattern=schema)
    info = client.get_flight_info(flight_descriptor(command), options)
    reader = client.do_get(info.endpoints[0].ticket, options)
    df = reader.read_pandas()
    return df['table_name'].tolist()

def flightsql_get_schema_names(client: flight.FlightClient,
                               options: Optional[flight.FlightCallOptions] = None) -> Tuple[List, List]:
    """Get the names of all schemas."""
    command = flightsql.CommandGetDbSchemas()
    info = client.get_flight_info(flight_descriptor(command), options)
    reader = client.do_get(info.endpoints[0].ticket, options)
    df = reader.read_pandas()
    return df['db_schema_name'].tolist()

def flightsql_get_sql_info(info: List[int],
                           client: flight.FlightClient,
                           options: Optional[flight.FlightCallOptions] = None) -> Dict[int, Any]:
    """Get metadata about the server and its SQL features."""
    command = flightsql.CommandGetSqlInfo(info=info)
    finfo = client.get_flight_info(flight_descriptor(command), options)
    reader = client.do_get(finfo.endpoints[0].ticket, options)
    values = reader.read_all().to_pylist()
    return {v['info_name']: v['value'] for v in values}

def flight_descriptor(inner: Any) -> flight.FlightDescriptor:
    """Create a FlightDescriptor for a command."""
    any = any_pb2.Any()
    any.Pack(inner)
    return flight.FlightDescriptor.for_command(any.SerializeToString())

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
        mapped_type = resolve_sql_type(t)
        description.append((schema.names[i], mapped_type))
    return description

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
