from enum import Enum
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Problem Types
# ---------------------------------------------------------

class ProblemType(str, Enum):
    ARITHMETIC = "ARITHMETIC"
    ALGEBRA = "ALGEBRA"
    CALCULUS = "CALCULUS"
    GEOMETRY = "GEOMETRY"
    TRIGONOMETRY = "TRIGONOMETRY"
    STATISTICS = "STATISTICS"
    PHYSICS = "PHYSICS"
    CHEMISTRY = "CHEMISTRY"
    LOGICAL_REASONING = "LOGICAL_REASONING"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------
# Status
# ---------------------------------------------------------

class ProblemStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    UNSUPPORTED = "UNSUPPORTED"


# ---------------------------------------------------------
# Detection Result
# ---------------------------------------------------------

class ProblemDetection(BaseModel):
    """
    Output produced by the detector.
    Only tells whether the query belongs to Problem Solver.
    """

    is_problem: bool = False

    problem_type: ProblemType = ProblemType.UNKNOWN

    # Original user query
    expression: str | None = None

    # Normalized mathematical expression
    normalized_expression: str | None = None


# ---------------------------------------------------------
# Final Result
# ---------------------------------------------------------

class ProblemResult(BaseModel):

    status: ProblemStatus = ProblemStatus.SUCCESS

    problem_type: ProblemType

    expression: str

    answer: str | None = None

    explanation: str | None = None

    error: str | None = None