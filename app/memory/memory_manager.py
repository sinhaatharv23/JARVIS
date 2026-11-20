"""
MEMORY MANAGER
==============

Coordinates the complete long-term memory pipeline.

Responsibilities
----------------
1. Analyze the user's latest message.
2. Execute the requested memory operation.
3. Return the final result.

The MemoryManager does NOT:
- Generate AI responses.
- Modify prompts.
- Write memory directly.
- Know how memories are stored.

It simply coordinates MemoryService and MemoryWriter.
"""

from typing import List,Dict,Any
import logging

from app.memory.memory_service import MemoryService
from app.memory.memory_writer import MemoryWriter

logger = logging.getLogger("J.A.R.V.I.S")


class MemoryManager:

    def __init__(
        self,
        memory_service: MemoryService,
        memory_writer: MemoryWriter,
    ):
        self.memory_service = memory_service
        self.memory_writer = memory_writer

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def process(self, user_message: str)->List[Dict[str,Any]]:
        """
        Complete memory pipeline.

        User Message
            │
            ▼
        MemoryService
            │
            ▼
        MemoryWriter
            │
            ▼
        Result(s)
        """

        logger.info("Starting memory pipeline...")

        # Step 1: Analyze the message
        existing_memories = self.memory_writer.list_memories()
        logger.info(
            "Existing memories passed to MemoryService:\n%s",
            existing_memories,
        )
        memories = self.memory_service.analyze(user_message,existing_memories,)
        logger.info(
            "MemoryService returned %d operation(s).",
            len(memories),
        )

        results = []

        # Step 2: Execute every memory operation
        for memory in memories:

            logger.info(
                "Memory decision -> %s | %s | %s",
                memory.get("operation"),
                memory.get("target_file"),
                memory.get("entry_key"),
            )

            result = self.memory_writer.execute(memory)

            results.append(result)

            logger.info(
                "Memory operation completed -> success=%s",
                result.get("success"),
            )

        logger.info(
            "Memory pipeline finished. %d operation(s) executed.",
            len(results),
        )

        return results