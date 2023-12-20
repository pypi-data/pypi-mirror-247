from calculator_mgaidy.calculator import Calculator
import pytest


@pytest.fixture
def calculator() -> Calculator:
    """Fixture to create an instance of the Calculator class."""
    return Calculator()


def test_add(calculator: Calculator) -> None:
    calculator.reset_memory()

    # Test a valid addition
    assert calculator.add(1) == 1

    # Test adding a number that exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.add(1e309)

    # Test adding a number that is below the minimum allowed value
    with pytest.raises(ValueError):
        calculator.add(-1e309)

    # Test checking if product result value exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.add(1e300)
        calculator.add(1e300)


def test_subtract(calculator: Calculator) -> None:
    calculator.reset_memory()

    # Test a valid subtraction
    assert calculator.subtract(5) == -5

    # Test subtracting number that exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.subtract(1e309)
    # Test subtracting a number that is below the minimum allowed value
    with pytest.raises(ValueError):
        calculator.subtract(-1e309)
    # Test checking if product result value exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.subtract(1e299)
        calculator.subtract(1e300)


def test_multiply(calculator: Calculator) -> None:
    calculator.reset_memory()

    # Test a valid subtraction
    calculator.add(1)
    assert calculator.multiply(11) == 11

    assert calculator.multiply(-11) == -121

    # Test multiplication number that exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.multiply(1e309)

    # Test multiplication a number that is below the minimum allowed value
    with pytest.raises(ValueError):
        calculator.multiply(-1e309)

    # Test checking if product result value exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.multiply(1e299)
        calculator.multiply(1e299)


def test_divide(calculator: Calculator) -> None:
    calculator.reset_memory()

    # Test a valid division
    calculator.add(0.1)
    assert calculator.divide(10) == 0.01

    assert calculator.divide(-10) == -0.001

    # Test invalid division by 0
    with pytest.raises(ValueError):
        calculator.divide(0)

    # Test division number that exceeds the maximum allowed value
    with pytest.raises(ValueError):
        calculator.divide(1e309)

    # Test division a number that is below the minimum allowed value
    with pytest.raises(ValueError):
        calculator.divide(-1e309)


def test_power(calculator: Calculator) -> None:
    calculator.reset_memory()

    # Test valid number to the power
    calculator.add(2)
    assert calculator.power(2) == 4

    assert calculator.power(0) == 1

    calculator.add(1)
    assert calculator.power(10) == 1024

    # Test invalid power
    with pytest.raises(ValueError):
        calculator.power(301)

    calculator.reset_memory()
    calculator.add(2)

    # Test negative power
    with pytest.raises(ValueError):
        calculator.power(-5)


def test_root(calculator: Calculator) -> None:
    calculator.reset_memory()

    # Test valid root
    assert calculator.root(2) == 0

    calculator.add(25)
    assert calculator.root(2) == 5

    # Test invalid negative roots
    with pytest.raises(ValueError):
        calculator.root(-5)

    # Test invalid roots power
    with pytest.raises(ValueError):
        calculator.root(301)


# Test valid inputs
def test_input_number_validation_valid(calculator: Calculator) -> None:
    valid_number: float = 100
    assert calculator.input_number_validation(valid_number) == valid_number


# Test invalid inputs
def test_input_number_validation_invalid(calculator: Calculator) -> None:

    # Test input number that exceeds the maximum allowed value
    invalid_number: float = 1e400
    with pytest.raises(ValueError):
        calculator.input_number_validation(invalid_number)

    # Test input number that is below the minimum allowed value
    invalid_number2: float = -1e400
    with pytest.raises(ValueError):
        calculator.input_number_validation(invalid_number2)


# Test invalid power
def test_input_power_validation_valid(calculator: Calculator) -> None:
    valid_power: float = 200
    assert calculator.input_power_validation(valid_power) == valid_power


# Test invalid power
def test_input_power_validation_invalid(calculator: Calculator) -> None:

    # Test power number that exceeds the maximum allowed value
    invalid_power: float = 400
    with pytest.raises(ValueError):
        calculator.input_power_validation(invalid_power)

    # Test division a number that is below the minimum allowed value
    invalid_power2: float = -1
    with pytest.raises(ValueError):
        calculator.input_power_validation(invalid_power2)


# Test valid results
def test_result_validation_valid(calculator: Calculator) -> None:

    valid_result: float = 1e200
    assert calculator.result_validation(valid_result) == valid_result

    valid_result1: float = 1e299
    assert calculator.result_validation(valid_result1) == valid_result1


# Test invalid results
def test_result_validation_invalid(calculator: Calculator) -> None:

    # Test result that exceeds the maximum allowed value
    invalid_result: float = 1e400
    with pytest.raises(ValueError):
        calculator.result_validation(invalid_result)

    # Test result that is below allowed value
    invalid_result2: float = -1e400
    with pytest.raises(ValueError):
        calculator.result_validation(invalid_result2)

    invalid_result3: float = -1e300 - 1e299
    with pytest.raises(ValueError):
        calculator.result_validation(invalid_result3)


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
    assert actual_log_len == expected_log_len


# Test history log learing
def test_history_log_clear(calculator: Calculator) -> None:
    expected_log_len: int = 0
    calculator.reset_memory()
    calculator.add(10)
    calculator.subtract(5)
    calculator.multiply(5)
    calculator.divide(25)
    calculator.add(1)
    calculator.power(2)
    calculator.root(2)
    calculator.clear_history_log()
    actual_log_len: int = len(calculator.logs)
    assert actual_log_len == expected_log_len


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
    assert expected_log_len == actual_log_len and calculator.memory == 0


# Test precision setter
def test_set_precision(calculator: Calculator) -> None:

    # Test setting valid precision
    calculator.set_precision(5)
    assert calculator.precision == 5

    # Test setting invalid precision
    with pytest.raises(ValueError):
        calculator.set_precision(-1)
