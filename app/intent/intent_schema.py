"""
INTENT SCHEMA
=============

Defines all shared data structures used by the Intent Engine.

This file contains:

1. IntentType
   - Every supported intent.

2. IntentSource
   - Where the intent came from.
     (Rule-based classifier or LLM)

3. IntentResult
   - Standard object returned by every
     intent detector.

Every module inside app.intent should import
these definitions instead of creating their own.
"""

from enum import Enum
from dataclasses import dataclass


# ==========================================================
# INTENT TYPES
# ==========================================================

class IntentType(str, Enum):
    """
    Every intent supported by J.A.R.V.I.S.

    New intents should always be added here first.
    """

    CHAT = "CHAT"

    MEMORY = "MEMORY"

    AUTOMATION = "AUTOMATION"

    SEARCH = "SEARCH"

    PLANNING = "PLANNING"

    CODING = "CODING"

    VISION = "VISION"

    UNKNOWN = "UNKNOWN"


# ==========================================================
# INTENT SOURCE
# ==========================================================

class IntentSource(str, Enum):
    """
    Where the detected intent came from.
    """

    RULE = "RULE"

    LLM = "LLM"


# ==========================================================
# INTENT RESULT
# ==========================================================

@dataclass
class IntentResult:
    """
    Standard result returned by every
    intent detector.

    Example
    -------

    IntentResult(
        intent=IntentType.MEMORY,
        confidence=1.0,
        source=IntentSource.RULE,
        reason="Message starts with 'remember'."
    )
    """

    intent: IntentType

    confidence: float

    source: IntentSource

    reason: str = ""