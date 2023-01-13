# This is a collection of tests that call out to a reference implemetation of
# Flight SQL. They aim to exercise the FlightSQLClient, DB API interface and
# SQLalchemy Dialect.
#
# Even though the upstream reference server isn't DataFusion (it's SQLite)
# we can still get pretty far when testing the DataFusion Dialect. We'll only be
# testing functionality here that's leveraging Flight SQL or where the syntactic
# differences between the SQLite and DataFusion dialects are the same.
#
# TODO(brett): We should eventually swap this server out with one backed by
# DataFusion that supports all of the functionality of Flight SQL.

import os
import pytest

import sqlalchemy.sql.sqltypes as sqltypes
from sqlalchemy import Column
from sqlalchemy import String, Integer
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.schema import MetaData, Table
from sqlalchemy import create_engine

import flightsql.sqlalchemy
from flightsql.dbapi import connect
from flightsql.client import FlightSQLClient
import flightsql.flightsql_pb2 as flightsql

integration_disabled_msg = "INTEGRATION not set to 1. Skipping."

def integration_disabled():
    return not (bool(os.getenv("INTEGRATION")) or False)

def host_port():
    host = os.getenv("FLIGHTSQL_SERVER_HOST") or "127.0.0.1"
    port = os.getenv("FLIGHTSQL_SERVER_PORT") or 3000
    return host, port

def new_client():
    host, port = host_port()
    return FlightSQLClient(host=host, port=port, insecure=True)

def new_sqlalchemy_engine():
    host, port = host_port()
    return create_engine(f"datafusion+flightsql://{host}:{port}?insecure=true")

def new_conn():
    return connect(new_client())

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_dialect_configuration():
    engine = new_sqlalchemy_engine()
    # Force the connection so we get our SQL information.
    engine.connect()
    info = engine.dialect.sql_info
    assert info[flightsql.FLIGHT_SQL_SERVER_READ_ONLY] is False

@pytest.mark.skipif(integration_disabled(), reason=integration_disabled_msg)
def test_integration_dialect_basic_orm():
    engine = new_sqlalchemy_engine()
    base = declarative_base()
    metadata = MetaData()

    class Record(base):
        __tablename__ = Table('intTable', metadata, autoload=True, autoload_with=engine)
        id = Column(Integer, primary_key=True)
        key_name = Column(Integer, name="keyName")
        value = Column(String)

    session = Session(engine)
    stmt = select(Record).where(Record.id.in_([1, 2, 3]))
    results = session.scalars(stmt).all()
    assert [r.key_name for r in results] == ["one", "zero", "negative one"]
    assert [r.value for r in results] == [1, 0, -1]

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
