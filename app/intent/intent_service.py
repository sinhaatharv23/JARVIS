"""
INTENT SERVICE
==============

Uses the LLM to classify user intent when the
rule-based IntentClassifier cannot determine it.

Responsibilities
----------------
- Analyze the user's latest message.
- Classify it into one supported intent.
- Return an IntentResult.

This service should ONLY be called when
IntentClassifier returns UNKNOWN.
"""

import json
import logging

from app.intent.intent_schema import (
    IntentResult,
    IntentSource,
    IntentType,
)

logger = logging.getLogger("J.A.R.V.I.S")


class IntentService:
    """
    LLM-powered intent classifier.
    """

    def __init__(self, groq_service):
        self.groq_service = groq_service

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def classify(self, user_message: str) -> IntentResult:

        system_prompt = """
You are the Intent Classifier for J.A.R.V.I.S.

Your ONLY responsibility is to classify the user's intent.

Return ONLY valid JSON.

==================================================
SUPPORTED INTENTS
==================================================

CHAT
MEMORY
AUTOMATION
SEARCH
PLANNING
CODING
VISION

==================================================
INTENT DEFINITIONS
==================================================

CHAT

General conversation.

Examples:

Hello

How are you?

Tell me a joke.

Explain recursion.

--------------------------------------------

MEMORY

The user wants to remember, update or remove
long-term information.

Examples:

Remember my birthday.

Forget my favourite movie.

My favourite IDE is Cursor.

--------------------------------------------

AUTOMATION

The user wants J.A.R.V.I.S. to perform an action.

Examples:

Open Chrome.

Launch VS Code.

Close Spotify.

Restart my PC.

--------------------------------------------

SEARCH

The user needs current or online information.

Examples:

Search Google for Python.

Search YouTube for Docker.

Latest AI news.

--------------------------------------------

PLANNING

The user wants help creating a plan,
roadmap or strategy.

Examples:

Create a roadmap for backend development.

Help me prepare for placements.

Plan my week.

--------------------------------------------

CODING

Programming-related tasks.

Examples:

Solve this LeetCode problem.

Debug my Python code.

Explain Binary Search.

--------------------------------------------

VISION

Image or visual understanding.

Examples:

Describe this image.

Explain this screenshot.

Read the text from this image.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY this JSON:

{
    "intent": "...",
    "confidence": 0.95,
    "reason": "..."
}

Rules

intent must be exactly one of:

CHAT
MEMORY
AUTOMATION
SEARCH
PLANNING
CODING
VISION

Do not return markdown.

Do not return explanations.

Do not return extra text.

Return only valid JSON.
"""

        try:

            response = self.groq_service.invoke_raw(
                system_prompt=system_prompt,
                user_prompt=user_message,
            )

            data = json.loads(response)

            return IntentResult(
                intent=IntentType(data["intent"]),
                confidence=float(data["confidence"]),
                source=IntentSource.LLM,
                reason=data.get("reason", ""),
            )

        except Exception as e:

            logger.exception(
                "Intent classification failed: %s",
                e,
            )

            return IntentResult(
                intent=IntentType.UNKNOWN,
                confidence=0.0,
                source=IntentSource.LLM,
                reason=str(e),
            )