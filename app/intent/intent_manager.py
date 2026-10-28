"""
INTENT MANAGER
==============

Coordinates the complete Intent Engine.

Pipeline
--------

User Message
      │
      ▼
IntentClassifier (Rules)
      │
      ├── Intent Found
      │        │
      │        ▼
      │    Return Result
      │
      └── UNKNOWN
               │
               ▼
        IntentService (LLM)
               │
               ▼
          Return Result

Responsibilities
----------------
- Call the rule-based classifier.
- Fall back to the LLM when needed.
- Return a unified IntentResult.
"""

import logging

from app.intent.intent_classifier import IntentClassifier
from app.intent.intent_service import IntentService
from app.intent.intent_schema import (
    IntentResult,
    IntentType,
)

logger = logging.getLogger("J.A.R.V.I.S")


class IntentManager:

    def __init__(
        self,
        classifier: IntentClassifier,
        intent_service: IntentService,
    ):
        self.classifier = classifier
        self.intent_service = intent_service

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def process(
        self,
        user_message: str,
    ) -> IntentResult:
        """
        Determine the user's intent.

        First tries the rule-based classifier.

        If no rule matches,
        falls back to the LLM.
        """

        logger.info("Starting intent pipeline...")

        # ------------------------------------------------------
        # Step 1
        # Rule-based classification
        # ------------------------------------------------------

        result = self.classifier.classify(user_message)

        logger.info(
            "Rule classifier -> intent=%s | confidence=%.2f",
            result.intent.value,
            result.confidence,
        )

        # ------------------------------------------------------
        # Step 2
        # If rule matched, return immediately
        # ------------------------------------------------------

        if result.intent != IntentType.UNKNOWN:

            logger.info(
                "Intent determined using rule-based classifier."
            )

            return result

        # ------------------------------------------------------
        # Step 3
        # Fallback to LLM
        # ------------------------------------------------------

        logger.info(
            "No rule matched. Falling back to LLM..."
        )

        result = self.intent_service.classify(user_message)

        logger.info(
            "LLM classifier -> intent=%s | confidence=%.2f",
            result.intent.value,
            result.confidence,
        )

        return result