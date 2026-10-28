import ast

from .calculator_exceptions import (InvalidExpressionError,)


class CalculatorValidator:
    """
    Validates AST before evaluation.

    Responsibilities
    ----------------
    • Prevent excessively deep expressions
    • Reject oversized expressions
    """

    MAX_AST_DEPTH = 50
    MAX_AST_NODES = 500

    @classmethod
    def validate(cls, tree: ast.AST) -> None:
        """
        Validate an AST.

        Raises
        ------
        InvalidExpressionError
        """

        depth = cls._depth(tree)

        if depth > cls.MAX_AST_DEPTH:
            raise InvalidExpressionError(
                f"Expression exceeds maximum depth ({cls.MAX_AST_DEPTH})."
            )

        nodes = sum(1 for _ in ast.walk(tree))

        if nodes > cls.MAX_AST_NODES:
            raise InvalidExpressionError(
                f"Expression exceeds maximum size ({cls.MAX_AST_NODES} nodes)."
            )

    @classmethod
    def _depth(cls, node: ast.AST) -> int:

        children = list(ast.iter_child_nodes(node))

        if not children:
            return 1

        return 1 + max(cls._depth(child) for child in children)