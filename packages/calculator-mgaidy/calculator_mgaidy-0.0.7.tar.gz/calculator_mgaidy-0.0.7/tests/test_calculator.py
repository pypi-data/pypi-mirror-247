from calculator_mgaidy.calculator import Calculator
import pytest


@pytest.fixture
def calculator() -> Calculator:
    """Fixture to create an instance of the Calculator class."""
    return Calculator()


# Test valid addition
def test_add_valid_number(calculator: Calculator) -> None:
    calculator.reset_memory()
    result: float = calculator.add(1)
    assert result == 1, f"Addition failed. Expected: 1, Got: {result}"


# Test adding a number that exceeds the maximum allowed value
def test_add_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.add(1e309)

    with pytest.raises(ValueError):
        calculator.reset_memory()
        calculator.add(1)
        calculator.add(1e300)
        calculator.add(1e299)


# Test adding a number that is below the minimum allowed value
def test_add_below_min_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.add(-1e309)


# Test checking if product result value exceeds the maximum allowed value
def test_result_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.add(1e300)
        calculator.add(1e300)


# Test a valid subtraction
def test_valid_subtraction(calculator: Calculator) -> None:
    calculator.reset_memory()
    result: float = calculator.subtract(5)
    assert result == -5, f"Subtraction failed. Expected: -5, Got: {result}"


# Test subtracting a number that exceeds the maximum allowed value
def test_subtract_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.subtract(1e309)

    with pytest.raises(ValueError):
        calculator.reset_memory()
        calculator.subtract(5)
        calculator.subtract(1e300)
        calculator.subtract(1e299)


# Test subtracting a number that is below the minimum allowed value
def test_subtract_below_min_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.subtract(-1e309)


# Test checking if product result value exceeds the maximum allowed value
def test_subtract_result_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.subtract(1e299)
        calculator.subtract(1e300)


# Test a valid multiplication
def test_valid_multiply(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    result: float = calculator.multiply(11)
    assert result == 11, f"Multiplication failed. Expected: 11, Got: {result}"


# Test multiplication of a negative number
def test_multiply_negative(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    result: float = calculator.multiply(-11)
    assert result == -11, (
        f'Multiplication of a negative number failed.'
        f'Expected: -11, Got: {result}')


# Test multiplication of a number that exceeds the maximum allowed value
def test_multiply_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    with pytest.raises(ValueError):
        calculator.multiply(1e309)


# Test multiplication of a number that is below the minimum allowed value
def test_multiply_below_min_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    with pytest.raises(ValueError):
        calculator.multiply(-1e309)


# Test checking if product result value exceeds the maximum allowed value
def test_multiply_result_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    with pytest.raises(ValueError):
        calculator.add(1e299)
        calculator.multiply(1e299)


# Test valid division
def test_valid_divide(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(0.1)
    result: float = calculator.divide(10)
    assert result == 0.01, f"Division failed. Expected: 0.01, Got: {result}"


# Test division of a negative number
def test_divide_negative(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(0.1)
    result: float = calculator.divide(-10)
    assert result == -0.01, (
        f"Negative division failed. Expected: -0.01, Got: {result}")


# Test invalid division by 0
def test_divide_by_zero(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(0.1)
    with pytest.raises(ValueError):
        calculator.divide(0)


# Test division with a number that exceeds the maximum allowed value
def test_divide_exceeds_max_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(100)
    with pytest.raises(ValueError):
        calculator.divide(1e301)


# Test division with a number that is below the minimum allowed value
def test_divide_below_min_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    with pytest.raises(ValueError):
        calculator.add(100)
        calculator.divide(-1e301)


# Test valid number to the power
def test_valid_power(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(2)
    result: float = calculator.power(2)
    assert result == 4, f"Power operation failed. Expected: 4, Got: {result}"


# Test power to zero
def test_power_to_zero(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(2)
    result: float = calculator.power(0)
    assert result == 1, f"Power to zero failed. Expected: 1, Got: {result}"


# Test invalid power
def test_invalid_power(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(2)
    with pytest.raises(ValueError):
        calculator.power(301)


# Test negative power
def test_negative_power(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(2)
    with pytest.raises(ValueError):
        calculator.power(-5)


# Test valid root from 0
def test_valid_root(calculator: Calculator) -> None:
    calculator.reset_memory()
    result: float = calculator.root(2)
    assert result == 0, f"Valid root failed. Expected: 0, Got: {result}"


# Test root with a value
def test_root_with_value(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(25)
    result: float = calculator.root(2)
    assert result == 5, f"Root operation failed. Expected: 5, Got: {result}"


# Test invalid negative roots
def test_invalid_negative_root(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    with pytest.raises(ValueError):
        calculator.root(-5)


# Test invalid roots power
def test_invalid_root_power(calculator: Calculator) -> None:
    calculator.reset_memory()
    calculator.add(1)
    with pytest.raises(ValueError):
        calculator.root(301)


# Test history log
def test_history_log(calculator: Calculator) -> None:
    expected_log_len: int = 7
    calculator.reset_memory()
    calculator.add(10)
    calculator.subtract(5)
    calculator.multiply(5)
    calculator.divide(25)
    calculator.add(1)
    calculator.power(2)
    calculator.root(2)
    actual_log_len: int = len(calculator.logs)
    assert actual_log_len == expected_log_len, (
        f'Failed correct history log.'
        f'Expected lengh: 7, Got: {actual_log_len}'
    )


# Test memory reset
def test_memory_reset(calculator: Calculator) -> None:
    expected_log_len: int = 0
    calculator.reset_memory()
    calculator.add(10)
    calculator.subtract(5)
    calculator.multiply(5)
    calculator.divide(25)
    calculator.add(1)
    calculator.power(2)
    calculator.root(2)
    calculator.reset_memory()
    actual_log_len: int = len(calculator.logs)
    assert expected_log_len == actual_log_len and calculator.memory == 0, (
        f'Failed to reset memory. Expected log lengh: 0, Got: {actual_log_len}'
        f'Expected memory value: 0, Got {calculator.memory}')


# Test setting valid precision
def test_set_valid_precision(calculator: Calculator) -> None:
    calculator.set_precision(5)
    assert calculator.precision == 5, (
        f'Failed to set precision. Expected: 5, Got: {calculator.precision}')


# Test setting negative precision
def test_set_invalid_precision(calculator: Calculator) -> None:
    with pytest.raises(ValueError):
        calculator.set_precision(-1)


# Test setting invalid precision
def test_maximum_precision(calculator: Calculator) -> None:
    with pytest.raises(ValueError):
        calculator.set_precision(301)


# Test if precision setting applied correctly
def test_correct_precision_setting(calculator: Calculator) -> None:
    expected_result: float = 2 / 3
    calculator.reset_memory()
    calculator.add(2)
    calculator.set_precision(11)
    actual_result: float = calculator.divide(3)
    assert round(actual_result, 11) == round(expected_result, 11), (
        f'Precision setting failed.'
        f'Expected:{round(expected_result, 11)}'
        f'Got:{round(actual_result, 11)}'
    )
