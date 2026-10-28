"""
PLANNER EXECUTOR
================

Executes a generated execution plan.

Responsibilities
----------------
- Execute plan steps sequentially.
- Return execution status.
- Delegate execution to the appropriate engine.

Current Version
---------------
V1 only simulates execution.

Future versions will delegate to:

- Automation Engine
- Coding Engine
- Memory Engine
- Vision Engine
- Search Engine
"""

import logging
from typing import Dict, Any, List

from app.planner.planner_schema import (
    Plan,
    PlanStep,
)

logger = logging.getLogger("J.A.R.V.I.S")


class PlannerExecutor:
    """
    Executes a generated plan.

    V1:
        Simulates execution.

    V2:
        Will call the appropriate engine
        for every step.
    """

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def execute(
        self,
        plan: Plan,
    ) -> Dict[str, Any]:

        logger.info(
            "Executing plan with %d step(s).",
            len(plan.steps),
        )

        completed_steps: List[Dict[str, Any]] = []

        for step in plan.steps:

            logger.info(
                "[STEP %d] %s",
                step.id,
                step.title,
            )

            # --------------------------------------------------
            # Future:
            #
            # Match step.engine and delegate
            # to Automation / Coding / Memory / etc.
            # --------------------------------------------------

            step.completed = True

            completed_steps.append(
                {
                    "id": step.id,
                    "title": step.title,
                    "engine": step.engine.value,
                    "status": "COMPLETED",
                }
            )

        logger.info(
            "Plan execution completed."
        )

        return {
            "success": True,
            "goal": plan.goal,
            "completed_steps": completed_steps,
            "total_steps": len(plan.steps),
        }