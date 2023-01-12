import os
import pytest
import flightsql.sqlalchemy
from flightsql.dbapi import connect
from flightsql.client import FlightSQLClient
import flightsql.flightsql_pb2 as flightsql
import sqlalchemy.sql.sqltypes as sqltypes

from sqlalchemy import create_engine

integration_disabled_msg = "INTEGRATION not set to 1. Skipping."

def integration_disabled():
    return not (bool(os.getenv("INTEGRATION")) or False)

def new_client():
    server_host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    server_port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000
    return FlightSQLClient(host=server_host, port=server_port, insecure=True)

def new_conn():
    return connect(new_client())

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_dialect_configuration():
    engine = create_engine("datafusion+flightsql://127.0.0.1:3000?insecure=true")

    # Force the connection so we get our SQL information.
    engine.connect()
    info = engine.dialect.sql_info
    assert info[flightsql.FLIGHT_SQL_SERVER_READ_ONLY] is False

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_update():
    client = new_client()

    update_query = "insert into intTable (id, keyName, value, foreignId) values (5, 'five', 5, 5)"
    result = client.execute_update(update_query)
    assert result == 1
    result = client.execute_update("delete from intTable where id = 5")
    assert result == 1

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_query():
    conn = new_conn()
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
    conn = new_conn()
    names = conn.flightsql_get_table_names(None)
    assert names == ['foreignTable',
                     'intTable',
                     'sqlite_sequence']
    conn.close()

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_sql_info():
    conn = new_conn()

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
    conn = new_conn()
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
    conn = new_conn()

    # SQLite doesn't support schemas, but we'll make sure its going through the
    # motions to arrive at an empty list.
    assert conn.flightsql_get_schema_names() == []
    conn.close()
