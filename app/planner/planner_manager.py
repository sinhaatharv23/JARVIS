"""
PLANNER MANAGER
===============

Coordinates the complete Planner pipeline.

Responsibilities
----------------
1. Generate a plan using PlannerService.
2. Convert the JSON into Plan objects.
3. Return the final Plan.

The PlannerManager does NOT:
- Execute the plan.
- Call Automation.
- Generate AI responses.

It simply coordinates PlannerService.
"""

import logging

from app.planner.planner_service import PlannerService
from app.planner.planner_schema import (
    Plan,
    PlanStep,
    Complexity,
    ExecutionEngine,
)

logger = logging.getLogger("J.A.R.V.I.S")


class PlannerManager:
    """
    Coordinates the Planner Engine.
    """

    def __init__(
        self,
        planner_service: PlannerService,
    ):
        self.planner_service = planner_service

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def process(
        self,
        user_message: str,
    ) -> Plan:
        """
        Complete planning pipeline.

        User Message
              │
              ▼
        PlannerService
              │
              ▼
          JSON Plan
              │
              ▼
        Convert to Objects
              │
              ▼
             Plan
        """

        logger.info("Starting planner pipeline...")

        # ------------------------------------------------------
        # Step 1
        # Generate JSON plan
        # ------------------------------------------------------

        result = self.planner_service.create_plan(
            user_message,
        )

        logger.info(
            "Planner returned %d step(s).",
            len(result.get("steps", [])),
        )

        # ------------------------------------------------------
        # Step 2
        # Convert steps
        # ------------------------------------------------------

        steps = []

        for step in result.get("steps", []):

            try:

                steps.append(

                    PlanStep(
                        id=step["id"],
                        title=step["title"],
                        description=step["description"],
                        engine=ExecutionEngine(
                            step["engine"]
                        ),
                    )

                )

            except Exception:

                logger.warning(
                    "Skipping invalid planner step: %s",
                    step,
                )

        # ------------------------------------------------------
        # Step 3
        # Build Plan
        # ------------------------------------------------------

        try:

            complexity = Complexity(
                result.get(
                    "complexity",
                    "LOW",
                )
            )

        except Exception:

            complexity = Complexity.LOW

        plan = Plan(

            goal=result.get(
                "goal",
                user_message,
            ),

            complexity=complexity,

            estimated_steps=result.get(
                "estimated_steps",
                len(steps),
            ),

            steps=steps,

        )

        logger.info(
            "Planner pipeline completed."
        )

        return plan