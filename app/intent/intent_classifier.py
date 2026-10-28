"""
INTENT CLASSIFIER
=================

Fast rule-based intent detection.

Responsibilities
----------------
- Detect obvious user intents.
- Avoid unnecessary LLM calls.
- Return an IntentResult.

This classifier should only contain
deterministic rules.

If no rule matches,
return UNKNOWN.

The IntentManager will then decide
whether to invoke the LLM.
"""

import re

from app.intent.intent_schema import (
    IntentType,
    IntentSource,
    IntentResult,
)


class IntentClassifier:
    """
    Fast rule-based intent detector.
    """

    # ==========================================================
    # KEYWORD TABLES
    # ==========================================================

    MEMORY_KEYWORDS = (
        "remember",
        "forget",
        "delete memory",
        "remove memory",
        "store",
        "save",
    )

    AUTOMATION_KEYWORDS = (
        "open",
        "launch",
        "start",
        "close",
        "shutdown",
        "restart",
        "minimize",
        "maximize",
    )

    SEARCH_KEYWORDS = (
        "search",
        "google",
        "look up",
        "find online",
        "search youtube",
        "search google",
    )

    CODING_KEYWORDS = (
        "leetcode",
        "codeforces",
        "debug",
        "bug",
        "algorithm",
        "dsa",
        "code",
        "python",
        "java",
        "c++",
        "javascript",
    )

    PLANNING_KEYWORDS = (
        "plan",
        "roadmap",
        "schedule",
        "strategy",
        "prepare",
        "goal",
    )

    VISION_KEYWORDS = (
        "image",
        "photo",
        "picture",
        "screenshot",
        "ocr",
        "camera",
        "describe this image",
    )

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def classify(self, message: str) -> IntentResult:
        """
        Detect the user's intent using rules.
        """

        text = message.strip().lower()

        # ---------------- MEMORY ----------------

        if self._contains(text, self.MEMORY_KEYWORDS):
            return IntentResult(
                intent=IntentType.MEMORY,
                confidence=1.0,
                source=IntentSource.RULE,
                reason="Matched memory keyword.",
            )

        # ---------------- AUTOMATION ----------------

        if self._contains(text, self.AUTOMATION_KEYWORDS):
            return IntentResult(
                intent=IntentType.AUTOMATION,
                confidence=1.0,
                source=IntentSource.RULE,
                reason="Matched automation keyword.",
            )

        # ---------------- SEARCH ----------------

        if self._contains(text, self.SEARCH_KEYWORDS):
            return IntentResult(
                intent=IntentType.SEARCH,
                confidence=1.0,
                source=IntentSource.RULE,
                reason="Matched search keyword.",
            )
        # ---------------- PLANNING ----------------

        if self._contains(text, self.PLANNING_KEYWORDS):
            return IntentResult(
                intent=IntentType.PLANNING,
                confidence=0.95,
                source=IntentSource.RULE,
                reason="Matched planning keyword.",
            )
        # ---------------- CODING ----------------

        if self._contains(text, self.CODING_KEYWORDS):
            return IntentResult(
                intent=IntentType.CODING,
                confidence=0.95,
                source=IntentSource.RULE,
                reason="Matched coding keyword.",
            )

        # ---------------- VISION ----------------

        if self._contains(text, self.VISION_KEYWORDS):
            return IntentResult(
                intent=IntentType.VISION,
                confidence=1.0,
                source=IntentSource.RULE,
                reason="Matched vision keyword.",
            )

        # ---------------- UNKNOWN ----------------

        return IntentResult(
            intent=IntentType.UNKNOWN,
            confidence=0.0,
            source=IntentSource.RULE,
            reason="No rule matched.",
        )

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _contains(
        self,
        text: str,
        keywords: tuple[str, ...],
    ) -> bool:
        """
        Returns True if any keyword is found
        as a whole word.
        """

        for keyword in keywords:

            pattern = rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, text):
                return True

        return False