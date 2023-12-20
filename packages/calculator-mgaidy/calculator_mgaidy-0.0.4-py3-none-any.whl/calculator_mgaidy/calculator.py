from math import fsum
from typing import List


class Calculator:
    """
    A basic calculator class that supports arithmetic operations and maintains
    a history log.

    Attributes:
        memory (float): The current memory value of the calculator.
        logs (List[str]): A list to store the history log of operations.
        precision (int): The precision to round results to.

    Constants:
        MAX_NUMBER (float): The maximum allowed number in calculations.
        MIN_NUMBER (float): The minimum allowed number in calculations.
        MAX_POWER_LEVEL (int): The maximum allowed power level for
                                                        exponentiation.
    """

    MAX_NUMBER = 1e300
    MIN_NUMBER: float = -1e300
    MAX_POWER_LEVEL = 300

    def __init__(self, memory: float = 0, precision: int = 10) -> None:
        """
        Initialize the Calculator.

        Args:
            memory (float, optional): Initial memory value. Defaults to 0.
            precision (int, optional): The precision to round results to.
                                                           Defaults to 10.
        """
        self.memory: float = memory
        self.logs: List[str] = []
        self.precision: int = precision

    def set_precision(self, precision: int) -> None:
        """
        Set the precision for rounding results.

        Args:
            precision (int): The precision to set. Must be a non-negative
                                                                  integer.

        Raises:
            ValueError: If precision is a negative integer.
        """
        if precision < 0:
            raise ValueError("Precision must be a non-negative integer.")
        self.precision = precision

    def history_log(self, symbol: str, number: float) -> List[str]:
        """
        Log an arithmetic operation to the history log.

        Args:
            symbol (str): The symbol representing the operation
                                            (+, -, *, /, ^, root).
            number (float): The operand involved in the operation.

        Returns:
            List[str]: The updated history log.
        """
        self.logs.append(f'{self.memory} {symbol} {number}\n')
        return self.logs

    def clear_history_log(self) -> None:
        """Clear the history log."""
        self.logs.clear()

    def reset_memory(self) -> float:
        """
        Reset the calculator memory to zero and clear the history log.

        Returns:
            float: The reset memory value (0).
        """
        self.memory = 0
        self.clear_history_log()
        return self.memory

    def input_number_validation(self, number: float) -> float:
        """
        Validate if the provided number is within the allowed range.

        Args:
            number (float): The number to validate.

        Returns:
            float: The validated number.

        Raises:
            ValueError: If the number is outside the allowed range.
        """
        if self.MIN_NUMBER > abs(number) or abs(number) > self.MAX_NUMBER:
            raise ValueError("Number value is not allowed.")
        return number

    def input_power_validation(self, power: float) -> float:
        """
        Validate if the provided power is within the allowed range.

        Args:
            power (float): The power to validate.

        Returns:
            float: The validated power.

        Raises:
            ValueError: If the power is outside the allowed range.
        """
        if 0 > power or power > self.MAX_POWER_LEVEL:
            raise ValueError("Power or root is too big.")
        return power

    def result_validation(self, result: float) -> float:
        """
        Validate if the result is within the allowed range.

        Args:
            result (float): The result to validate.

        Returns:
            float: The validated result.

        Raises:
            ValueError: If the result is outside the allowed range.
        """
        if abs(result) < self.MIN_NUMBER or abs(result) > self.MAX_NUMBER:
            raise ValueError("Result value is too long to display.")
        return result

    def add(self, number: float) -> float:
        """
        Add a number to the calculator memory.

        Args:
            number (float): The number to add.

        Returns:
            float: The result of the addition.
        """
        self.input_number_validation(number)
        result: float = fsum([self.memory, number])
        self.result_validation(result)
        self.history_log("+", number)
        self.memory = result
        return round(result, self.precision)

    def subtract(self, number: float) -> float:
        """
        Subtract a number from the calculator memory.

        Args:
            number (float): The number to subtract.

        Returns:
            float: The result of the subtraction.

        Raises:
            ValueError: If the provided number is outside the allowed range.
        """
        self.input_number_validation(number)
        result: float = fsum([self.memory, -1*number])
        self.result_validation(result)
        self.history_log("-", number)
        self.memory = result
        return round(result, self.precision)

    def multiply(self, number: float) -> float:
        """
        Multiply the calculator memory by a number.

        Args:
            number (float): The number to multiply by.

        Returns:
            float: The result of the multiplication.

        Raises:
            ValueError: If the provided number is outside the allowed range.
        """
        self.input_number_validation(number)
        result: float = self.memory * number
        self.result_validation(result)
        self.history_log("*", number)
        self.memory = result
        return round(result, self.precision)

    def divide(self, number: float) -> float:
        """
        Divide the calculator memory by a number.

        Args:
            number (float): The number to divide by.

        Returns:
            float: The result of the division.

        Raises:
            ValueError: If the provided number is outside the allowed range
            or division by zero is attempted.
        """
        self.input_number_validation(number)
        if number != 0:
            result: float = self.memory / number
            self.result_validation(result)
            self.history_log("/", number)
            self.memory = result
            return round(result, self.precision)
        raise ValueError("Division by 0 is not allowed")

    def power(self, number: float) -> float:
        """
        Raise the calculator memory to the power of a given number.

        Args:
            number (float): The power to raise the memory to.

        Returns:
            float: The result of the exponentiation.

        Raises:
            ValueError: If the provided power is outside the allowed range.
        """
        self.input_power_validation(number)
        result: float = self.memory ** number
        self.result_validation(result)
        self.history_log("^", number)
        self.memory = result
        return round(result, self.precision)

    def root(self, number: float) -> float:
        """
        Calculate the root of the calculator memory with a given exponent.

        Args:
            number (float): The exponent for the root operation.

        Returns:
            float: The result of the root operation.

        Raises:
            ValueError: If the provided exponent is outside the allowed range.
        """
        self.input_power_validation(number)
        result: float = self.memory ** (1/number)
        self.result_validation(result)
        self.history_log("root", number)
        self.memory = result
        return round(result, self.precision)
