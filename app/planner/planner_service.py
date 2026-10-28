"""
PLANNER SERVICE
===============

Uses the LLM to convert a user's request into
a structured execution plan.

Responsibilities
----------------
- Analyze the user's request.
- Break it into logical steps.
- Estimate complexity.
- Return structured JSON.

This service DOES NOT:
- Execute any steps.
- Perform automation.
- Generate the final answer.
"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger("J.A.R.V.I.S")


class PlannerService:
    """
    Planner Service

    Uses the Groq LLM to generate
    a structured execution plan.
    """

    def __init__(self, groq_service):
        self.groq_service = groq_service

    def create_plan(
        self,
        user_message: str,
    ) -> Dict[str, Any]:
        """
        Generate an execution plan.

        Returns a dictionary matching
        planner_schema.Plan.
        """

        system_prompt = """
You are the Planning Engine of J.A.R.V.I.S.

Your ONLY responsibility is to break the user's request
into a logical sequence of executable steps.

Return ONLY valid JSON.

==================================================
RULES
==================================================

1. Understand the user's goal.

2. Estimate complexity.

Possible values:

LOW
MEDIUM
HIGH

3. Break the task into logical steps.

Each step must contain:

- id
- title
- description
- engine

==================================================
AVAILABLE ENGINES
==================================================

CHAT
MEMORY
AUTOMATION
CODING
SEARCH
VISION
HUMAN

Choose the BEST engine for every step.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

{
    "goal": "...",
    "complexity": "...",
    "estimated_steps": number,
    "steps": [
        {
            "id": 1,
            "title": "...",
            "description": "...",
            "engine": "..."
        }
    ]
}

==================================================
IMPORTANT
==================================================

Do not execute anything.

Do not explain.

Do not answer the user.

Do not write markdown.

Return ONLY JSON.
"""

        try:

            response = self.groq_service.invoke_raw(
                system_prompt=system_prompt,
                user_prompt=user_message,
            )

            try:
                result = json.loads(response)

            except json.JSONDecodeError:

                logger.error(
                    "Invalid JSON returned by PlannerService:\n%s",
                    response,
                )

                return {
                    "goal": user_message,
                    "complexity": "LOW",
                    "estimated_steps": 0,
                    "steps": [],
                }

            logger.info(
                "Planner created %d step(s).",
                len(result.get("steps", [])),
            )

            return result

        except Exception as e:

            logger.exception(
                "Planner generation failed: %s",
                e,
            )

            return {
                "goal": user_message,
                "complexity": "LOW",
                "estimated_steps": 0,
                "steps": [],
            }