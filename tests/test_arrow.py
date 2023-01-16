from flightsql.arrow import ParameterRecordBuilder
from flightsql.exceptions import Error
from pytest import raises

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
