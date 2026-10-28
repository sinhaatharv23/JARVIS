from .arithmetic_detector import ArithmeticDetector
from .calculator_executor import CalculatorExecutor

from .problem_schema import (
    ProblemResult,
    ProblemStatus,
    ProblemType,
)


class ProblemSolverManager:
    """
    Entry point for the Arithmetic Solver.

    Responsibilities
    ----------------
    • Detect arithmetic problems.
    • Execute calculations.
    • Return a ProblemResult.

    The manager never performs calculations itself.
    """

    def __init__(
        self,
        detector: ArithmeticDetector | None = None,
        executor: CalculatorExecutor | None = None,
    ) -> None:

        self.detector = (
            detector
            if detector is not None
            else ArithmeticDetector()
        )

        self.executor = (
            executor
            if executor is not None
            else CalculatorExecutor()
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def solve(self, query: str) -> ProblemResult:
        """
        Solve an arithmetic query.

        Parameters
        ----------
        query : str

        Returns
        -------
        ProblemResult
        """

        if not query or not query.strip():

            return ProblemResult(
                status=ProblemStatus.FAILED,
                problem_type=ProblemType.UNKNOWN,
                expression=query or "",
                answer=None,
                explanation=None,
                error="Query cannot be empty.",
            )

        # ------------------------------------------------------
        # Detect
        # ------------------------------------------------------

        detection = self.detector.detect(query)

        # ------------------------------------------------------
        # Not an arithmetic problem
        # ------------------------------------------------------

        if not detection.is_problem:

            return ProblemResult(
                status=ProblemStatus.UNSUPPORTED,
                problem_type=ProblemType.UNKNOWN,
                expression=query,
                answer=None,
                explanation=None,
                error="Query is not an arithmetic problem.",
            )

        # ------------------------------------------------------
        # Execute
        # ------------------------------------------------------

        return self.executor.execute(detection)