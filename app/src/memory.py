from collections import defaultdict


class MemoryManager:
    def __init__(self):
        self.sessions = defaultdict(list)

    def add_message(self, session_id: str, message: dict):
        self.sessions[session_id].append(message)

    def get_session_history(self, session_id: str) -> list:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]