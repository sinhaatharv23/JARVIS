from .problem_schema import (
    ProblemDetection,
    ProblemResult,
    ProblemStatus,
    ProblemType,
)

from .calculator_service import CalculatorService

from .calculator_exceptions import CalculatorError


class CalculatorExecutor:
    """
    Executes arithmetic calculations.

    Responsibilities
    ----------------
    • Accept a ProblemDetection object.
    • Validate the detection.
    • Delegate evaluation to CalculatorService.
    • Convert calculator responses into ProblemResult.

    Never performs calculations itself.
    """

    def __init__(
        self,
        calculator_service: CalculatorService | None = None,
    ) -> None:

        self.calculator_service = (
            calculator_service
            if calculator_service is not None
            else CalculatorService()
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def execute(
        self,
        detection: ProblemDetection,
    ) -> ProblemResult:
        """
        Execute an arithmetic problem.

        Parameters
        ----------
        detection : ProblemDetection

        Returns
        -------
        ProblemResult
        """

        # ------------------------------------------------------
        # Validate detection
        # ------------------------------------------------------

        if not detection.is_problem:
            return ProblemResult(
                status=ProblemStatus.UNSUPPORTED,
                problem_type=ProblemType.UNKNOWN,
                expression=detection.expression or "",
                answer=None,
                explanation=None,
                error="The supplied query is not an arithmetic problem.",
            )

        if detection.problem_type != ProblemType.ARITHMETIC:
            return ProblemResult(
                status=ProblemStatus.UNSUPPORTED,
                problem_type=detection.problem_type,
                expression=detection.expression or "",
                answer=None,
                explanation=None,
                error=(
                    f"Unsupported problem type "
                    f"'{detection.problem_type.value}'."
                ),
            )

        if not detection.normalized_expression:
            return ProblemResult(
                status=ProblemStatus.FAILED,
                problem_type=detection.problem_type,
                expression=detection.expression or "",
                answer=None,
                explanation=None,
                error="Normalized expression is missing.",
            )

        # ------------------------------------------------------
        # Execute calculation
        # ------------------------------------------------------

        try:

            answer = self.calculator_service.evaluate(
                detection.normalized_expression
            )

            return ProblemResult(
                status=ProblemStatus.SUCCESS,
                problem_type=detection.problem_type,
                expression=detection.expression or "",
                answer=str(answer),
                explanation=None,
                error=None,
            )

        except CalculatorError as error:

            return ProblemResult(
                status=ProblemStatus.FAILED,
                problem_type=detection.problem_type,
                expression=detection.expression or "",
                answer=None,
                explanation=None,
                error=str(error),
            )

        except Exception as error:

            return ProblemResult(
                status=ProblemStatus.FAILED,
                problem_type=detection.problem_type,
                expression=detection.expression or "",
                answer=None,
                explanation=None,
                error=f"Unexpected error: {error}",
            )