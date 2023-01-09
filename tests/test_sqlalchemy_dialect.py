from sqlalchemy.sql import sqltypes
from flightsql.sqlalchemy import resolve_sql_type

def test_resolve_arrow_type_string():
    cases = [
        ("timestamp(nanosecond, none)", sqltypes.TIMESTAMP),
        ("dictionary(int32, utf8)", sqltypes.TEXT),
        ("utf8", sqltypes.TEXT),
        ("bool", sqltypes.BOOLEAN),
    ]
    for (actual, expected) in cases:
        assert resolve_sql_type(actual) == expected
