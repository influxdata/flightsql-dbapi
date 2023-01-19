import pyarrow as pa
from pytest import raises
from sqlalchemy.sql import sqltypes

from flightsql.dbapi import ParameterRecordBuilder, dbapi_results, resolve_sql_type
from flightsql.exceptions import Error


def test_parameter_record_builder():
    params = [20, "hello", 3.14, b"data", True]
    builder = ParameterRecordBuilder(params)
    record = builder.build_record()

    assert record.num_rows == 1
    assert record.num_columns == 5
    assert record.column(0).to_pylist() == [20]
    assert record.column(1).to_pylist() == ["hello"]
    assert record.column(2).to_pylist() == [3.14]
    assert record.column(3).to_pylist() == [b"data"]
    assert record.column(4).to_pylist() == [True]


def test_parameter_record_builder_unsupported_type():
    class Something:
        pass

    params = [Something()]
    builder = ParameterRecordBuilder(params)
    with raises(Error) as err:
        builder.build_record()
    assert str(err.value) == 'unable to map "Something" type to PyArrow datatype'
    assert err.type == Error


def test_dbapi_results():
    days = pa.array([1, 12, 17, 23, 28], type=pa.int8())
    months = pa.array([1, 3, 5, 7, 1], type=pa.int8())
    years = pa.array([1990, 2000, 1995, 2000, 1995], type=pa.int16())
    names = pa.array(["john", "jim", "jack", "jake", "jerry"], type=pa.string())
    table = pa.table([days, months, years, names], names=["days", "months", "years", "names"])
    values, descriptions = dbapi_results(table)

    assert values == [
        [1, 1, 1990, "john"],
        [12, 3, 2000, "jim"],
        [17, 5, 1995, "jack"],
        [23, 7, 2000, "jake"],
        [28, 1, 1995, "jerry"],
    ]
    assert descriptions == [
        ("days", sqltypes.INTEGER),
        ("months", sqltypes.INTEGER),
        ("years", sqltypes.INTEGER),
        ("names", sqltypes.TEXT),
    ]


def test_resolve_sql_type():
    cases = [
        (pa.timestamp("ns"), sqltypes.TIMESTAMP),
        (pa.time64("ns"), sqltypes.TIME),
        (pa.date64(), sqltypes.DATE),
        (pa.decimal128(5, 10), sqltypes.DECIMAL),
        (pa.string(), sqltypes.TEXT),
        (pa.utf8(), sqltypes.TEXT),
        (pa.float32(), sqltypes.FLOAT),
        (pa.float64(), sqltypes.FLOAT),
        (pa.int8(), sqltypes.INTEGER),
        (pa.int16(), sqltypes.INTEGER),
        (pa.int32(), sqltypes.INTEGER),
        (pa.int64(), sqltypes.BIGINT),
        (pa.uint8(), sqltypes.INTEGER),
        (pa.uint16(), sqltypes.INTEGER),
        (pa.uint32(), sqltypes.INTEGER),
        (pa.uint64(), sqltypes.BIGINT),
        (pa.bool_(), sqltypes.BOOLEAN),
        (pa.binary(), sqltypes.BINARY),
    ]
    for (actual, expected) in cases:
        assert resolve_sql_type(actual) == expected
