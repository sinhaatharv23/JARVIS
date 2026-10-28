"""
ORCHESTRATOR ROUTER
===================

Maps intents to the subsystem responsible
for handling them.

Responsibilities
----------------
- Receive an IntentType.
- Return the RouteType.
- Do NOT execute any business logic.
"""

from app.intent.intent_schema import IntentType
from app.orchestrator.orchestrator_schema import RouteType


class OrchestratorRouter:
    """
    Maps IntentType -> RouteType.
    """

    # ==========================================================
    # ROUTE TABLE
    # ==========================================================

    ROUTES = {
        IntentType.CHAT: RouteType.CHAT,
        IntentType.MEMORY: RouteType.MEMORY,
        IntentType.AUTOMATION: RouteType.AUTOMATION,
        IntentType.SEARCH: RouteType.SEARCH,
        IntentType.PLANNING: RouteType.PLANNER,
        IntentType.CODING: RouteType.CHAT,
        IntentType.VISION: RouteType.VISION,
        IntentType.UNKNOWN: RouteType.UNKNOWN,
    }

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def route(self, intent: IntentType) -> RouteType:
        """
        Return the destination subsystem
        for the detected intent.
        """

        return self.ROUTES.get(
            intent,
            RouteType.UNKNOWN,
        )