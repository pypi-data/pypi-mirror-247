import doctest
from math import exp, log


class Calculator:
    """
    Calculator class
    ...
    Attributes:
        __number : int
            Own memory of the calculator. All the operations will be
            performed on this number
    ...
    Methods:
        add(other_number: float) -> float
            adds other_number to a number
        subtract(other_number: float) -> float
            subtracts other_number from a number
        multiply(other_number: float) -> float
            multiplies other_number by a number
        divide(other_number: float) -> float
            divides other_number by a number
        nth_root(other_number: int) -> float
            takes n-th root of a number
        reset() -> float
            resets the number to 0
    """
    def __init__(self, number: float = 0.0):
        """
        :param number: float
        """
        self.__number = number

    @property
    def number(self) -> float:
        """
        Set a property for a number attribute
        """
        return self.__number

    def add(self, other_number: float) -> float:
        """
        Adds other_number to a number and returns the result
        :param other_number: float
        :return: float
        For example:
        >>> calc = Calculator(10)
        >>> calc.add(5)
        15
        """
        self.__number += other_number
        return self.__number

    def subtract(self, other_number: float) -> float:
        """
        Subtracts other_number from a number and returns the result
        :param other_number: float
        :return: float
        For example:
        >>> calc = Calculator(10)
        >>> calc.subtract(5)
        5
        """
        self.__number -= other_number
        return self.__number

    def multiply(self, other_number: float) -> float:
        """
        Multiplies other_number by a number and returns the result
        :param other_number: float
        :return: float
        For example:
        >>> calc = Calculator(10)
        >>> calc.multiply(5)
        50
        """
        self.__number *= other_number
        return self.__number

    def divide(self, other_number: float) -> float:
        """
        Divides other_number by a number and returns the result.
        If other_number is 0, raise ZeroDivisionError.
        :param other_number: float
        :return: float
        For example:
        >>> calc = Calculator(10)
        >>> calc.divide(5)
        2.0
        """
        if other_number == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        self.__number /= other_number
        return self.__number

    def nth_root(self, n: int) -> float:
        """
        Takes n-th root of a number and returns the result.
        If the number is less than 0 and n is even, raise ValueError.
        :param n: int
        :return: float
        For example:
        >>> calc = Calculator(10)
        >>> calc.nth_root(2)
        3.1622776601683795
        """
        if self.number < 0 and n % 2 == 0:
            raise ValueError("Can't take an even root from a negative number")
        # use exp and log functions to print real number for the nth root of a negative number
        if self.__number != 0:
            self.__number = exp(log(abs(self.__number))/n) * (-1 if self.__number < 0 else 1)
        return self.__number

    def reset(self) -> float:
        """
        Resets the number to 0
        :return: float
        For example:
            >>> calc = Calculator(10)
            >>> calc.reset()
            0.0
        """
        self.__number = 0.0
        return self.__number


if __name__ == "__main__":
    calc = Calculator()
    print(calc.nth_root(65))
    print(doctest.testmod())
