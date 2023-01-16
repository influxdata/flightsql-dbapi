from typing import Tuple, Any, Union, List

import pyarrow as pa
from sqlalchemy import types
from flightsql.exceptions import Error

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

class ParameterRecordBuilder:
    """
    Builds a PyArrow RecordBatch from a list of parameters for prepared
    statements.
    """

    union_positions = {t: idx for idx, t in enumerate([int, float, str, bytes, bool])}
    arrow_types = {
        int: pa.int64,
        float: pa.float64,
        str: pa.utf8,
        bytes: pa.binary,
        bool: pa.bool_
    }

    def __init__(self, values: Union[Tuple[Any, ...], List[Any]]):
        self.values = values

    def union_array_for_value(self, value: Any) -> pa.UnionArray:
        """Builds a PyArrow UnionArray around a value."""
        pytype = type(value)
        if pytype not in self.union_positions:
            raise Error(f"unable to map \"{pytype.__name__}\" type to PyArrow datatype")

        children = []
        type_id = -1
        for t, idx in self.union_positions.items():
            arrow_type = self.arrow_types[t]()
            if t == pytype:
                type_id = idx
                values = [value]
            else:
                values = []
            children.append(pa.array(values, type=arrow_type))

        return pa.UnionArray.from_dense(pa.array([type_id], type=pa.int8()),
                                        pa.array([0], type=pa.int32()),
                                        children)

    def build_record(self) -> pa.RecordBatch:
        """
        Builds a PyArrow RecordBatch containing UnionArrays for all parameters.
        """
        if len(self.values) == 0:
            return pa.RecordBatch.from_arrays([], names=[])

        columns = [self.union_array_for_value(v) for v in self.values]
        names = [f"param_{i}" for i in range(len(columns))]
        return pa.RecordBatch.from_arrays(columns, names=names)
