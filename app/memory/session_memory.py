class SessionMemory:
    def __init__(self):
        self.session = {}

    def add(self, session_id:str, role:str, content:str):
        self.session.setdefault(session_id, []).append(
            {
                "role": role,
                "content": content
            }
        )

    def get(self, session_id:str):
        return self.session.get(session_id, [])

    def clear(self, session_id:str):
        self.session.pop(session_id, None)