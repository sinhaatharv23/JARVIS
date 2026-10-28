import re

from .problem_schema import (
    ProblemDetection,
    ProblemType,
)


class ArithmeticDetector:
    """
    Detects and normalizes arithmetic expressions.

    Responsibilities:
    -----------------
    1. Detect arithmetic problems.
    2. Normalize natural-language expressions.
    3. Extract evaluable expressions.

    Never performs calculations.
    """

    NORMALIZATION_PATTERNS = [

        # -----------------------------
        # Remove helper words
        # -----------------------------
        (r"\bwhat is\b", ""),
        (r"\bwhat's\b", ""),
        (r"\bcalculate\b", ""),
        (r"\bcompute\b", ""),
        (r"\bevaluate\b", ""),
        (r"\bfind\b", ""),
        (r"\bplease\b", ""),
        (r"\bjarvis\b", ""),
        (r"\bgive me\b", ""),
        (r"\banswer\b", ""),
        (r"\bthe\b", ""),

        # -----------------------------
        # Operators
        # -----------------------------
        (r"\bplus\b", "+"),
        (r"\bminus\b", "-"),
        (r"\btimes\b", "*"),
        (r"\bmultiplied by\b", "*"),
        (r"\bmultiply by\b", "*"),
        (r"\binto\b", "*"),

        (r"\bdivided by\b", "/"),
        (r"\bdivide by\b", "/"),

        (r"\bmodulus\b", "%"),
        (r"\bmod\b", "%"),

        (r"\braised to the power of\b", "**"),
        (r"\braised to\b", "**"),
        (r"\bpower of\b", "**"),

        # -----------------------------
        # Shortcuts
        # -----------------------------
        (r"(\d+)\s+squared", r"\1**2"),
        (r"(\d+)\s+cubed", r"\1**3"),

        (r"square root of\s+(\d+)", r"sqrt(\1)"),

        (r"half of\s+(\d+)", r"(\1/2)"),
        (r"quarter of\s+(\d+)", r"(\1/4)"),

        (r"(\d+)\s*%\s*of\s*(\d+)", r"(\1/100)*\2"),
    ]

    OPERATOR_PATTERN = re.compile(
        r"[\+\-\*/%()]|\*\*|sqrt"
    )

    def detect(self, query: str) -> ProblemDetection:

        if not query or not query.strip():
            return ProblemDetection(
                is_problem=False,
                problem_type=ProblemType.UNKNOWN,
            )

        original_query = query.strip()

        normalized = original_query.lower()

        # ----------------------------------------
        # Normalize
        # ----------------------------------------

        for pattern, replacement in self.NORMALIZATION_PATTERNS:
            normalized = re.sub(
                pattern,
                replacement,
                normalized,
                flags=re.IGNORECASE,
            )

        normalized = re.sub(r"\s+", " ", normalized).strip()

        # ----------------------------------------
        # Detect arithmetic
        # ----------------------------------------

        if not self.OPERATOR_PATTERN.search(normalized):
            return ProblemDetection(
                is_problem=False,
                problem_type=ProblemType.UNKNOWN,
            )

        # ----------------------------------------
        # Extract expression
        # ----------------------------------------

        expression = re.sub(
            r"[^0-9a-zA-Z\.\+\-\*\/%\(\)]",
            "",
            normalized,
        )

        expression = expression.strip()

        if not expression:
            return ProblemDetection(
                is_problem=False,
                problem_type=ProblemType.UNKNOWN,
            )

        return ProblemDetection(
            is_problem=True,
            problem_type=ProblemType.ARITHMETIC,
            expression=original_query,
            normalized_expression=expression,
        )