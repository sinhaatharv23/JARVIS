from pathlib import Path
import json

from config import CHATS_DATA_DIR


class ChatHistory:

    def __init__(self):
        self.chats_dir = Path(CHATS_DATA_DIR)

    def list_sessions(self):
        sessions = []

        for filepath in self.chats_dir.glob("chat_*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    chat_data = json.load(f)

                sessions.append({
                    "session_id": chat_data.get("session_id"),
                    "messages": chat_data.get("messages", []),
                })

            except (OSError, json.JSONDecodeError):
                continue

        return sessions