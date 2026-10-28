"""
PLANNER SCHEMA
==============

Shared data models used by the Planner Engine.

Responsibilities
----------------
- Define plan complexity.
- Define execution engines.
- Define a single plan step.
- Define the complete execution plan.

This file contains NO business logic.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ==========================================================
# COMPLEXITY
# ==========================================================

class Complexity(str, Enum):
    """
    Estimated difficulty of the user's request.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ==========================================================
# EXECUTION ENGINE
# ==========================================================

class ExecutionEngine(str, Enum):
    """
    Which subsystem should execute a step.
    """

    CHAT = "CHAT"

    MEMORY = "MEMORY"

    AUTOMATION = "AUTOMATION"

    CODING = "CODING"

    SEARCH = "SEARCH"

    VISION = "VISION"

    HUMAN = "HUMAN"

    UNKNOWN = "UNKNOWN"


# ==========================================================
# PLAN STEP
# ==========================================================

@dataclass
class PlanStep:
    """
    Represents a single executable step in a plan.
    """

    id: int

    title: str

    description: str

    engine: ExecutionEngine

    completed: bool = False


# ==========================================================
# COMPLETE PLAN
# ==========================================================

@dataclass
class Plan:
    """
    Represents the complete execution plan.
    """

    goal: str

    complexity: Complexity

    estimated_steps: int

    steps: List[PlanStep] = field(default_factory=list)