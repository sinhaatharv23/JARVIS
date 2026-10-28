class CalculatorError(Exception):
    """Base exception for all calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when an expression is invalid."""
    pass


class UnsupportedOperatorError(CalculatorError):
    """Raised when an unsupported operator is encountered."""
    pass


class UnsupportedFunctionError(CalculatorError):
    """Raised when an unsupported function is called."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero occurs."""
    pass