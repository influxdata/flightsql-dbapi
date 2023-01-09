import pyarrow as pa
from sqlalchemy import types

def resolve_sql_type(t: pa.DataType):
    """Resolves an Arrow DataType value to a SQL type."""

    if pa.types.is_timestamp(t): return types.TIMESTAMP
    if pa.types.is_time(t): return types.TIME
    if pa.types.is_date(t): return types.DATE
    if pa.types.is_binary(t): return types.BINARY
    if pa.types.is_boolean(t): return types.BOOLEAN
    if pa.types.is_decimal(t): return types.DECIMAL
    if pa.types.is_floating(t): return types.FLOAT
    if pa.types.is_string(t): return types.TEXT

    if pa.types.is_signed_integer(t) and not pa.types.is_int64(t):
        return types.INTEGER
    if pa.types.is_int64(t):
        return types.BIGINT

    # TODO(brett): Find a way to deal with unsigned integers.
    if pa.types.is_unsigned_integer(t) and not pa.types.is_uint64(t):
        return types.INTEGER
    if pa.types.is_uint64(t):
        return types.BIGINT

    # TODO(brett): I'd like to be permissive of unknown types here, but I'm not
    # sure what type we should fall back to.
    return types.BLOB
