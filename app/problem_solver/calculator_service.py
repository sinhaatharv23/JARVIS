import ast
from typing import Any

from .calculator_registry import (
    BINARY_OPERATORS,
    UNARY_OPERATORS,
    FUNCTIONS,
    CONSTANTS,
)

from .calculator_validator import CalculatorValidator

from .calculator_exceptions import (
    CalculatorError,
    DivisionByZeroError,
    InvalidExpressionError,
    UnsupportedFunctionError,
    UnsupportedOperatorError,
)


class CalculatorService:
    """
    Production-grade AST based calculator.

    Features
    --------
    ✔ Secure (No eval)
    ✔ AST based evaluation
    ✔ Immutable operator registry
    ✔ Custom exceptions
    ✔ AST validation
    ✔ Extensible
    """

    def evaluate(self, expression: str) -> int | float:
        """
        Safely evaluate an arithmetic expression.

        Parameters
        ----------
        expression : str

        Returns
        -------
        int | float

        Raises
        ------
        CalculatorError
        """

        if not expression or not expression.strip():
            raise InvalidExpressionError(
                "Expression cannot be empty."
            )

        try:
            # Parse the expression into an AST
            tree = ast.parse(expression, mode="eval")

            # Validate AST before evaluation
            CalculatorValidator.validate(tree)

            # Evaluate recursively
            result = self._evaluate(tree.body)

            # Return integers cleanly
            if isinstance(result, float) and result.is_integer():
                return int(result)

            return result

        except ZeroDivisionError:
            raise DivisionByZeroError(
                "Division by zero is not allowed."
            )

        except CalculatorError:
            raise

        except SyntaxError:
            raise InvalidExpressionError(
                "Invalid expression syntax."
            )

        except Exception as e:
            raise InvalidExpressionError(str(e))

    # ==========================================================
    # Internal Recursive Evaluator
    # ==========================================================

    def _evaluate(self, node: ast.AST) -> Any:

        # ------------------------------------------------------
        # Numeric Constants
        # ------------------------------------------------------

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise InvalidExpressionError(
                "Only numeric constants are allowed."
            )

        # Python < 3.8 compatibility
        if isinstance(node, ast.Num):
            return node.n

        # ------------------------------------------------------
        # Named Constants
        # ------------------------------------------------------

        if isinstance(node, ast.Name):

            if node.id in CONSTANTS:
                return CONSTANTS[node.id]

            raise InvalidExpressionError(
                f"Unknown identifier '{node.id}'."
            )

        # ------------------------------------------------------
        # Binary Operations
        # ------------------------------------------------------

        if isinstance(node, ast.BinOp):

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            operator_type = type(node.op)

            if operator_type not in BINARY_OPERATORS:
                raise UnsupportedOperatorError(
                    f"Unsupported operator '{operator_type.__name__}'."
                )

            return BINARY_OPERATORS[operator_type](
                left,
                right,
            )

        # ------------------------------------------------------
        # Unary Operations
        # ------------------------------------------------------

        if isinstance(node, ast.UnaryOp):

            operand = self._evaluate(node.operand)

            operator_type = type(node.op)

            if operator_type not in UNARY_OPERATORS:
                raise UnsupportedOperatorError(
                    f"Unsupported unary operator '{operator_type.__name__}'."
                )

            return UNARY_OPERATORS[operator_type](operand)

        # ------------------------------------------------------
        # Function Calls
        # ------------------------------------------------------

        if isinstance(node, ast.Call):

            if not isinstance(node.func, ast.Name):
                raise InvalidExpressionError(
                    "Invalid function call."
                )

            function_name = node.func.id

            if function_name not in FUNCTIONS:
                raise UnsupportedFunctionError(
                    f"Unsupported function '{function_name}'."
                )

            arguments = [
                self._evaluate(argument)
                for argument in node.args
            ]

            return FUNCTIONS[function_name](*arguments)

        # ------------------------------------------------------
        # Reject Everything Else
        # ------------------------------------------------------

        raise InvalidExpressionError(
            f"Unsupported syntax '{type(node).__name__}'."
        )