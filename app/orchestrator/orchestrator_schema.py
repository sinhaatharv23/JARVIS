"""
ORCHESTRATOR SCHEMA
===================

Shared data models used by the Orchestrator.

This file defines:

1. RouteType
   - Every destination that the Orchestrator
     can forward a request to.

2. OrchestratorResult
   - Standard result returned by the
     Orchestrator before execution.
"""

from enum import Enum
from dataclasses import dataclass


# ==========================================================
# ROUTE TYPES
# ==========================================================

class RouteType(str, Enum):
    """
    Every subsystem inside J.A.R.V.I.S.
    """

    CHAT = "CHAT"

    MEMORY = "MEMORY"

    AUTOMATION = "AUTOMATION"

    SEARCH = "SEARCH"

    PLANNER = "PLANNER"

    CODING = "CODING"

    VISION = "VISION"

    UNKNOWN = "UNKNOWN"


# ==========================================================
# ORCHESTRATOR RESULT
# ==========================================================

@dataclass
class OrchestratorResult:
    """
    Result returned by the Orchestrator.

    route:
        Destination subsystem.

    reason:
        Why this route was selected.
    """

    route: RouteType

    reason: str = ""