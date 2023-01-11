import pyarrow as pa
from sqlalchemy.sql import sqltypes
from flightsql.dbapi import dbapi_results
from flightsql.arrow import resolve_sql_type

def test_dbapi_results():
    days = pa.array([1, 12, 17, 23, 28], type=pa.int8())
    months = pa.array([1, 3, 5, 7, 1], type=pa.int8())
    years = pa.array([1990, 2000, 1995, 2000, 1995], type=pa.int16())
    names = pa.array(["john", "jim", "jack", "jake", "jerry"], type=pa.string())
    table = pa.table([days, months, years, names],
                     names=["days", "months", "years", "names"])
    values, descriptions = dbapi_results(table)

    assert values == [
        [1, 1, 1990, "john"],
        [12, 3, 2000, "jim"],
        [17, 5, 1995, "jack"],
        [23, 7, 2000, "jake"],
        [28, 1, 1995, "jerry"],
    ]
    assert descriptions == [
        ('days', sqltypes.INTEGER),
        ('months', sqltypes.INTEGER),
        ('years', sqltypes.INTEGER),
        ('names', sqltypes.TEXT),
    ]

def test_resolve_sql_type():
    cases = [
        (pa.timestamp('ns'), sqltypes.TIMESTAMP),
        (pa.time64('ns'), sqltypes.TIME),
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
