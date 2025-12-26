import json
import os
from datetime import datetime
from time import timezone

class LongTermMemory:
    def __init__(self, path="long_term_memory.json"):
        self.path = path

    def record(self, event: dict):
        event["timestamp"] = datetime.now().isoformat()
        data = []

        if os.path.exists(self.path):
            with open(self.path) as f:
                data = json.load(f)

        data.append(event)

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
