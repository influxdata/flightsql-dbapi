import os
import pytest
from flightsql.dbapi import connect
from flightsql.flight import create_client
import flightsql.flightsql_pb2 as flightsql
import sqlalchemy.sql.sqltypes as sqltypes

integration_disabled_msg = "INTEGRATION not set to 1. Skipping."

def integration_disabled():
    return not (bool(os.getenv("INTEGRATION")) or False)

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_dbapi_query():
    server_host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    server_port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000

    conn = connect(*create_client(host=server_host,
                                  port=server_port,
                                  insecure=True))
    cursor = conn.cursor()
    cursor.execute('select * from intTable')

    assert cursor.description == [
        ('id', sqltypes.BIGINT),
        ('keyName', sqltypes.TEXT),
        ('value', sqltypes.BIGINT),
        ('foreignId', sqltypes.BIGINT),
    ]
    assert [r for r in cursor] == [
        [1, 'one', 1.0, 1.0],
        [2, 'zero', 0.0, 1.0],
        [3, 'negative one', -1.0, 1.0],
        [4, None, None, None],
    ]
    conn.close()

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_get_table_names():
    server_host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    server_port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000

    conn = connect(*create_client(host=server_host,
                                  port=server_port,
                                  insecure=True))

    names = conn.flightsql_get_table_names(None)
    assert names == ['foreignTable',
                     'intTable',
                     'sqlite_sequence']
    conn.close()

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_sql_info():
    server_host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    server_port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000

    conn = connect(*create_client(host=server_host,
                                  port=server_port,
                                  insecure=True))

    # Some servers respond with a full set of information if an empty list is
    # provided. This SQLite reference implementation seems to require specific
    # codes to be requested.
    info = conn.flightsql_get_sql_info([
        flightsql.FLIGHT_SQL_SERVER_NAME,
        flightsql.FLIGHT_SQL_SERVER_VERSION,
        flightsql.FLIGHT_SQL_SERVER_ARROW_VERSION,
        flightsql.FLIGHT_SQL_SERVER_READ_ONLY,
    ])
    assert info[flightsql.FLIGHT_SQL_SERVER_NAME] == 'db_name'
    assert info[flightsql.FLIGHT_SQL_SERVER_VERSION] == 'sqlite 3'
    assert info[flightsql.FLIGHT_SQL_SERVER_ARROW_VERSION] == '11.0.0-SNAPSHOT'
    assert info[flightsql.FLIGHT_SQL_SERVER_READ_ONLY] is False
    conn.close()

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_get_columns():
    server_host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    server_port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000

    conn = connect(*create_client(host=server_host,
                                  port=server_port,
                                  insecure=True))
    columns = conn.flightsql_get_columns('intTable', None)
    assert columns == [
        {
            'name': 'id',
            'type': sqltypes.BIGINT,
            'default': None,
            'comment': None,
            'nullable': False,
            },
        {
            'name': 'keyName',
            'type': sqltypes.TEXT,
            'default': None,
            'comment': None,
            'nullable': False,
            },
        {
            'name': 'value',
            'type': sqltypes.BIGINT,
            'default': None,
            'comment': None,
            'nullable': False,
            },
        {
            'name': 'foreignId',
            'type': sqltypes.BIGINT,
            'default': None,
            'comment': None,
            'nullable': False,
        },
    ]
    conn.close()

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_get_schema_names():
    server_host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    server_port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000

    conn = connect(*create_client(host=server_host,
                                  port=server_port,
                                  insecure=True))

    # SQLite doesn't support schemas, but we'll make sure its going through the
    # motions to arrive at an empty list.
    assert conn.flightsql_get_schema_names() == []
    conn.close()
