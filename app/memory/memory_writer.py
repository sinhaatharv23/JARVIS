"""
MEMORY WRITER
=============

Version 1

Responsibilities
----------------
- Write new memories into the correct txt file.
- Prevent duplicate entries.
- Save updated files.

(No section parsing in V1)
"""

from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger("J.A.R.V.I.S")


class MemoryWriter:

    def __init__(self, learning_data_dir: Path):
        self.learning_data_dir = learning_data_dir

    # ==========================================================
    # FILE HELPERS
    # ==========================================================

    def get_file_path(self, filename: str) -> Path:
        return self.learning_data_dir / filename

    def load_text(self, filename: str) -> str:

        path = self.get_file_path(filename)

        if not path.exists():
            raise FileNotFoundError(path)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def save_text(self, filename: str, content: str):

        path = self.get_file_path(filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # ==========================================================
    # LIST MEMORIES
    # ==========================================================

    def list_memories(self) -> str:

        output = []

        for file in sorted(self.learning_data_dir.glob("*.txt")):

            output.append(f"\n===== {file.stem.upper()} =====")

            text = self.load_text(file.name)

            start = self.find_auto_memory_start(text)

            if start is None:
                output.append("No learned memories.")
                continue

            auto = text[start:]

            lines = auto.splitlines()

            collecting = False

            for line in lines:

                if "AUTO LEARNED MEMORIES" in line:
                    collecting = True
                    continue

                if not collecting:
                    continue

                line = line.strip()

                if (
                    not line
                    or line.startswith("=")
                ):
                    continue

                output.append(line)

        return "\n".join(output)

    # ==========================================================
    # BUILD MEMORY BLOCK
    # ==========================================================

    def build_memory(
        self,
        key: str,
        value: str,
    ) -> str:

        return f"{key}:\n{value}\n"
    # ==========================================================
    # NORMALIZE KEY
    # ==========================================================

    def normalize_key(self, key: str) -> str:

        aliases = {
    "programming font": "Favourite Programming Font",
    "coding font": "Favourite Programming Font",
    "favourite font": "Favourite Programming Font",
    "favourite programming font": "Favourite Programming Font",

    "ide": "Favourite IDE",
    "favourite ide": "Favourite IDE",

    "movie": "Favourite Movie",
    "favourite movie": "Favourite Movie",

    "book": "Favourite Book",
    "favourite book": "Favourite Book",

    "song": "Favourite Song",
    "favourite song": "Favourite Song",

    "food": "Favourite Food",
    "favourite food": "Favourite Food",

    "colour": "Favourite Colour",
    "color": "Favourite Colour",
    "favourite colour": "Favourite Colour",
    "favorite color": "Favourite Colour",
        }

        cleaned = key.strip().lower()

        return aliases.get(cleaned, key)

    # ==========================================================
    # APPEND MEMORY
    # ==========================================================

    def append_memory(
        self,
        existing_text: str,
        key: str,
        value: str,
    ) -> str:

        block = self.build_memory(key, value)

        if "AUTO LEARNED MEMORIES" not in existing_text:

            existing_text += (
                "\n"
                "=========================================\n"
                "AUTO LEARNED MEMORIES\n"
                "=====================\n\n"
            )

        if not existing_text.endswith("\n"):
            existing_text += "\n"

        existing_text += block
        existing_text += "\n"

        return existing_text
    # ==========================================================
    # FIND AUTO MEMORY SECTION
    # ==========================================================

    def find_auto_memory_start(self, text: str):

        marker = "AUTO LEARNED MEMORIES"

        index = text.find(marker)

        if index == -1:
            return None

        return index

    # ==========================================================
    # REPLACE MEMORY
    # ==========================================================

    def replace_memory(
        self,
        existing_text: str,
        key: str,
        value: str,
    ) -> str:

        start = self.find_auto_memory_start(existing_text)

        # No AUTO section -> append instead
        if start is None:
            return self.append_memory(
                existing_text,
                key,
                value,
            )

        before = existing_text[:start]
        auto = existing_text[start:]

        lines = auto.splitlines()

        found = False

        i = 0

        while i < len(lines):

            if lines[i].strip().lower() == f"{key}:".lower():

                # Replace only the value line
                if i + 1 < len(lines):
                    lines[i + 1] = value
                else:
                    lines.append(value)

                found = True
                break

            i += 1

        # Key doesn't exist -> append inside AUTO section
        if not found:

            if lines and lines[-1] != "":
                lines.append("")

            lines.append(f"{key}:")
            lines.append(value)

        return before + "\n".join(lines)
    # ==========================================================
    # FIND EXISTING VALUE
    # ==========================================================

    def get_existing_value(
        self,
        existing_text: str,
        key: str,
    ):

        start = self.find_auto_memory_start(existing_text)

        if start is None:
            return None

        auto = existing_text[start:]

        lines = auto.splitlines()

        for i in range(len(lines) - 1):

            if lines[i].strip().lower() == f"{key}:".lower():
                return lines[i + 1].strip()

        return None
    # ==========================================================
    # DELETE MEMORY
    # ==========================================================

    def delete_memory(
        self,
        target_file: str,
        key: str,
    ) -> Dict[str, Any]:

        key = self.normalize_key(key)

        text = self.load_text(target_file)

        start = self.find_auto_memory_start(text)

        if start is None:
            return {
                "success": False,
                "reason": "AUTO LEARNED MEMORIES section not found."
            }

        before = text[:start]
        auto = text[start:]

        lines = auto.splitlines()

        new_lines = []

        found = False
        skip_next = False

        for line in lines:

            if skip_next:
                skip_next = False
                found = True
                continue

            if line.strip().lower() == f"{key}:".lower():
                skip_next = True
                continue

            new_lines.append(line)

        if not found:
            return {
                "success": False,
                "reason": "Memory not found."
            }

        updated_text = before + "\n".join(new_lines)

        self.save_text(
            target_file,
            updated_text,
        )

        return {
            "success": True,
            "updated": True,
            "target_file": target_file,
            "operation": "DELETE",
            "reason": "Memory deleted successfully."
        }
    # ==========================================================
    # MAIN FUNCTION
    # ==========================================================

    # ==========================================================
    # PUBLIC ENTRY POINT
    # ==========================================================

    def execute(
        self,
        memory: Dict[str, Any],
    ) -> Dict[str, Any]:

        operation = memory.get("operation", "IGNORE").upper()

        logger.info("Memory operation requested -> %s", operation)

        if operation == "IGNORE":
            return {
                "success": True,
                "updated": False,
                "operation": "IGNORE",
                "reason": "No memory update required."
            }

        if operation == "DELETE":
            return self.delete_memory(
                memory["target_file"],
                memory["entry_key"],
            )

        return self._store_memory(memory)
    
    def _store_memory(
        self,
        memory: Dict[str, Any],
    ) -> Dict[str, Any]:
        
        target_file = memory["target_file"]
        key = memory["entry_key"]
        value = memory["entry_value"]
        if not key or not value:
            return {
                "success": False,
                "updated": False,
                "reason": "Invalid memory: missing key or value.",
            }
        key = self.normalize_key(key)
        logger.info(
            "Writing memory -> %s | %s=%s",
            target_file,
            key,
            value,
        )

        text = self.load_text(target_file)
        existing_value = self.get_existing_value(
            text,
            key,
        )

        # New memory
        if existing_value is None:

            updated_text = self.append_memory(
                text,
                key,
                value,
            )

            operation = "append"

        # Same value already stored
        elif existing_value.lower() == value.lower():

            return {
                "success": True,
                "updated": False,
                "target_file": target_file,
                "operation": "ignore",
                "reason": "Memory already exists.",
            }

        # Existing key but different value
        else:

            updated_text = self.replace_memory(
                text,
                key,
                value,
            )

            operation = "replace"
        self.save_text(
            target_file,
            updated_text,
        )

        logger.info(
            "Memory written successfully -> %s",
            target_file,
        )

        return {
            "success": True,
            "updated": True,
            "target_file": target_file,
            "operation": operation,
            "reason": "Memory stored successfully.",
        }