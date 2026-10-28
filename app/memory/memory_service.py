"""
MEMORY SERVICE MODULE
=====================

Phase 1:
---------
This service determines whether the user's latest message contains
long-term information worth remembering.

Responsibilities:
- Analyze ONLY the latest user message.
- Decide whether it should become permanent memory.
- Suggest which knowledge file should be updated.
- Return structured JSON.

This service DOES NOT:
- Update any txt files.
- Rebuild the vector store.
- Modify chat history.

Those responsibilities will be handled in later phases.
"""

import json
import logging
from typing import Dict, Any,List

logger = logging.getLogger("J.A.R.V.I.S")


class MemoryService:
    """
    Memory Analyzer

    Uses the Groq LLM to determine whether the user's latest
    message contains important long-term information.
    """

    def __init__(self, groq_service):
        self.groq_service = groq_service

    def analyze(self, user_message: str) -> List[Dict[str, Any]]:
        """
        Analyze the user's latest message.

        Returns:
        {
            "operation": str,

            # Allowed values:
            # ADD
            # UPDATE
            # DELETE
            # IGNORE

            "target_file": str | None,
            "section": str | None,
            "entry_key": str | None,
            "entry_value": str | None,
            "reason": str,
            "confidence": float
        }
        """

        system_prompt = """
You are the Memory Manager of J.A.R.V.I.S.

Your ONLY job is to determine whether the user's latest message
contains long-term information worth remembering.

Return ONLY valid JSON.

==================================================
AVAILABLE KNOWLEDGE FILES
==================================================

userdata.txt
family.txt
relationship.txt
education.txt
career.txt
skills.txt
projects.txt
goals.txt
preferences.txt
health.txt
hobbies.txt
achievements.txt

==================================================
FILE DESCRIPTIONS
==================================================

userdata.txt
- Core identity about Atharva.

family.txt
- ONLY Atharva's family members.

relationship.txt
- Friends and friendship information.
- Everything related to Aashu (Aastha Tarco), her family,
  your relationship, anniversaries, important memories,
  relationship milestones and future plans.

education.txt
- Academic information.

skills.txt
- Technical skills and technologies.

projects.txt
- Software projects.

career.txt
- Career updates.

goals.txt
- Long-term goals.

preferences.txt
- Communication preferences.
- Personal preferences.
- Favourite IDE
- Favourite Programming Font
- Favourite Movie
- Favourite Book
- Favourite Song
- Favourite Food
- Favourite Colour
- Favourite Sport
- Favourite Game
- Favourite Animal


health.txt
- Health information.


hobbies.txt
- Hobbies and interests.

achievements.txt
- Awards and accomplishments.


==================================================
REMEMBER
==================================================

Remember information such as:

- Personal identity
- Family members
- Relationship information
- Education
- Career
- Skills
- Goals
- Health updates
- Long-term hobbies
- Favorites
- Achievements
- Stable personal preferences
- Important life events

Relationship information includes:

- Aashu
- Aashu's family
- Relationship milestones
- Relationship events
-Friend's information
==================================================
DO NOT REMEMBER
==================================================

Do NOT remember:

- Greetings
- Small talk
- Temporary emotions
- Daily routine
- Food
- Weather
- Random opinions
- Questions
- Jokes
- One-time requests
- Information that already exists in the knowledge base
- Secrets, passwords, OTPs or confidential credentials.
==================================================
OUTPUT FORMAT
==================================================

Return ONLY a valid JSON array.

If there are no memories:

[]

If there is one memory:

[
   {...}
]

If there are multiple:

[
   {...},
   {...},
   {...}
]

The JSON MUST contain exactly these keys:

- operation (string)
    Allowed values

    ADD
    UPDATE
    DELETE
    IGNORE
- target_file (string or null)
- section (string or null)
- entry_key (string or null)
- entry_value (string or null)
- reason (string)
- confidence (number between 0 and 1)

Rules:
1. If the message contains new long-term information:

- operation = "ADD"

If the message changes an existing long-term memory,
return

operation = "UPDATE"

Examples

"My favourite IDE is now Cursor."

"I changed my favourite movie to Inception."

"I now weigh 72 kilograms."


If the user explicitly requests removing a stored memory,
return

operation = "DELETE"

Examples

"Forget my favourite IDE."

"Remove my favourite movie."

"Delete my weight."

"Don't remember my favourite colour anymore."



If the user's message does not contain any long-term information,
or is a greeting, question, temporary statement, joke,
or casual conversation,

return

operation = "IGNORE"

- target_file = the most appropriate knowledge file.

- section = the most appropriate section inside that file.

- entry_key

    The label that should appear inside the section.

    Examples:

    Mother's Name
    Father's Name
    Birthday
    Company
    Skill
    Goal
    Favourite Movie
    Hobby

- entry_value

    ONLY the value corresponding to entry_key.

Examples:

Message:

"Anna is my friend."


Return:

entry_key = "Friend's Name"

entry_value = "Anna"

Message:
"Aashu's mother's name is Rakhi Tarco."

Return:

entry_key = "Mother's Name"

entry_value = "Rakhi Tarco"

----------------------------

Message:

"I started learning Docker."

Return:

entry_key = "Skill"

entry_value = "Docker"

----------------------------

Message:

"My favorite movie is Interstellar."

Return:

entry_key = "Favourite Movie"

entry_value = "Interstellar"

==================================================
CANONICAL MEMORY KEYS
==================================================

Always use ONLY the following key names.

Never invent a new key.
Never shorten a key.
Never use synonyms.

Identity
--------
Name
Nickname
Birthday
Age

Family
------
Mother's Name
Father's Name
Brother's Name
Sister's Name

Relationship
------------
Partner's Name
Friend's Name
Anniversary
Relationship Status

Preferences
-----------
Favourite IDE
Favourite Programming Font
Favourite Movie
Favourite Book
Favourite Song
Favourite Food
Favourite Colour
Favourite Sport
Favourite Game
Favourite Animal

Career
------
Company
Role
Skill
Project
Goal

Health
------
Height
Weight

Education
---------
Degree
College
University
Branch
CGPA

Hobbies
-------
Hobby

Rules:

If the user says:

"My favourite programming font is Fira Code."

Return

entry_key = "Favourite Programming Font"

NOT

Programming Font

NOT

Favourite Font

----------------------------------------

If the user says:

"My favourite IDE is IntelliJ IDEA."

Return

entry_key = "Favourite IDE"

NOT

IDE

----------------------------------------

If the user says:

"I started learning Docker."

Return

entry_key = "Skill"

entry_value = "Docker"

----------------------------------------

Always reuse an existing canonical key if one matches the user's information.

Never invent a different key name for the same type of information.

If a canonical key exists for the information,
ALWAYS use that key exactly.

Never create variations in spelling,
capitalization, wording or formatting.

The same fact must always produce
the same entry_key.


==================================================


2. If the message should NOT be remembered:

- operation = "IGNORE"

- target_file = null

- section = null

- entry_key = null

- entry_value = null

Do not include markdown.
Do not include explanations.
Do not wrap the JSON inside ``` blocks.


==================================================
DECISION PROCESS
==================================================

For every message:

Step 1.
Determine whether the message contains long-term information.

Step 2.
If yes, determine whether the user is:

- adding new information
- updating existing information
- deleting existing information

Step 3.
Choose exactly one operation:

ADD
UPDATE
DELETE
IGNORE

Step 4.
Populate the remaining JSON fields.

Never invent information.
Never guess.



If operation is "IGNORE", ALWAYS return:

target_file = null

section = null

entry_key = null

entry_value = null

Never populate these fields when operation is IGNORE.


Never wrap the JSON in markdown.
Never return explanations before or after the JSON.
Never use ```json or ``` fences.

The response must be parseable directly by Python's json.loads().



Never invent new operation names.
"""

        try:

            response = self.groq_service.invoke_raw(
                system_prompt=system_prompt,
                user_prompt=user_message
            )

            try:
                result = json.loads(response)

                # Backward compatibility:
                # If a single object is returned, convert it to a list.
                if isinstance(result, dict):
                    result = [result]

                logger.info(
                    "MemoryService returned %d memory operation(s).",
                    len(result),
                )

                for memory in result:
                    logger.info(
                        "Operation=%s | File=%s | Key=%s | Confidence=%s",
                        memory.get("operation"),
                        memory.get("target_file"),
                        memory.get("entry_key"),
                        memory.get("confidence"),
                    )

                return result

            except json.JSONDecodeError:

                logger.error(
                    "Invalid JSON returned by MemoryService:\n%s",
                    response,
                )

                return [
                    {
                        "operation": "IGNORE",
                        "target_file": None,
                        "section": None,
                        "entry_key": None,
                        "entry_value": None,
                        "reason": "Invalid JSON returned by LLM.",
                        "confidence": 0.0,
                    }
                ]

        except Exception as e:

            logger.exception("Memory analysis failed: %s", e)

            return [
                {
                    "operation": "IGNORE",
                    "target_file": None,
                    "section": None,
                    "entry_key": None,
                    "entry_value": None,
                    "reason": f"Memory analysis failed: {str(e)}",
                    "confidence": 0.0,
                }
            ]