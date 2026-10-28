"""
ORCHESTRATOR
============

The central coordinator of J.A.R.V.I.S.

Responsibilities
----------------
1. Determine the user's intent.
2. Route the intent to the correct subsystem.
3. Return the selected route.

The Orchestrator does NOT:

- Generate AI responses.
- Perform memory operations.
- Execute automation.
- Plan tasks.
- Search the web.

It simply coordinates the different engines.
"""

import logging

from app.intent.intent_manager import IntentManager
from app.orchestrator.orchestrator_router import OrchestratorRouter
from app.orchestrator.orchestrator_schema import (
    OrchestratorResult,
)

logger = logging.getLogger("J.A.R.V.I.S")


class Orchestrator:
    """
    Coordinates the complete J.A.R.V.I.S. pipeline.
    """

    def __init__(
        self,
        intent_manager: IntentManager,
        router: OrchestratorRouter,
    ):
        self.intent_manager = intent_manager
        self.router = router

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def process(
        self,
        user_message: str,
    ) -> OrchestratorResult:
        """
        Complete orchestration pipeline.

        User Message
              │
              ▼
        Intent Manager
              │
              ▼
        Orchestrator Router
              │
              ▼
        Route
        """

        logger.info("Starting orchestration pipeline...")

        # ------------------------------------------------------
        # Step 1
        # Detect Intent
        # ------------------------------------------------------

        intent = self.intent_manager.process(user_message)

        logger.info(
            "Detected Intent -> %s",
            intent.intent.value,
        )

        # ------------------------------------------------------
        # Step 2
        # Determine Route
        # ------------------------------------------------------

        route = self.router.route(
            intent.intent,
        )

        logger.info(
            "Selected Route -> %s",
            route.value,
        )

        # ------------------------------------------------------
        # Step 3
        # Return Result
        # ------------------------------------------------------

        return OrchestratorResult(
            route=route,
            reason=intent.reason,
        )