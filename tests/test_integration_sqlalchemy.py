import pytest
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql import compiler

import flightsql.flightsql_pb2 as flightsql
from flightsql.sqlalchemy import FEATURE_PREPARED_STATEMENTS, LiteralBindCompiler

from . import integration


def new_sqlalchemy_engine(features={}):
    host, port = integration.host_port()
    query = {"insecure": "true"}
    for k, v in features.items():
        query[f"feature-{k}"] = v
    url = URL.create(drivername="datafusion+flightsql", host=host, port=int(port), query=query)
    return create_engine(url)


@pytest.mark.skipif(integration.is_disabled(), reason=integration.disabled_message)
def test_integration_dialect_configuration():
    engine = new_sqlalchemy_engine()
    # Force the connection so we get our SQL information.
    engine.connect()
    info = engine.dialect.sql_info
    assert info[flightsql.FLIGHT_SQL_SERVER_READ_ONLY] is False
    assert info[flightsql.FLIGHT_SQL_SERVER_NAME] == "db_name"
    assert info[flightsql.FLIGHT_SQL_SERVER_ARROW_VERSION] == "11.0.0-SNAPSHOT"


@pytest.mark.skipif(integration.is_disabled(), reason=integration.disabled_message)
def test_integration_dialect_basic_orm():
    engine = new_sqlalchemy_engine()
    base = declarative_base()
    metadata = MetaData()

    # Connect to ensure we're using the literal binding compiler.
    engine.connect()
    assert engine.dialect.statement_compiler == LiteralBindCompiler

    class Record(base):
        __tablename__ = Table("intTable", metadata, autoload=True, autoload_with=engine)
        id = Column(Integer, primary_key=True)
        key_name = Column(Integer, name="keyName")
        value = Column(String)

    session = Session(engine)
    stmt = select(Record).where(Record.id.in_([1, 2, 3]))
    results = session.scalars(stmt).all()
    assert [r.key_name for r in results] == ["one", "zero", "negative one"]
    assert [r.value for r in results] == [1, 0, -1]


@pytest.mark.skipif(integration.is_disabled(), reason=integration.disabled_message)
def test_integration_dialect_basic_orm_with_prepared_statements():
    engine = new_sqlalchemy_engine(features={FEATURE_PREPARED_STATEMENTS: "on"})
    base = declarative_base()
    metadata = MetaData()

    # Connect to ensure we're using the default compiler.
    engine.connect()
    assert engine.dialect.statement_compiler == compiler.SQLCompiler

    class Record(base):
        __tablename__ = Table("intTable", metadata, autoload=True, autoload_with=engine)
        id = Column(Integer, primary_key=True)
        key_name = Column(Integer, name="keyName")
        value = Column(String)

    session = Session(engine)
    stmt = select(Record).where(Record.id.in_([1, 2, 3]))
    results = session.scalars(stmt).all()
    assert [r.key_name for r in results] == ["one", "zero", "negative one"]
    assert [r.value for r in results] == [1, 0, -1]
