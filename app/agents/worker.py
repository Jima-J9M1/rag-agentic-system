import requests

LLM_MODEL = "llama3"

class WorkerAgent:
    def __init__(self, name: str):
        self.name = name

    def answer(self, query: str, context: list[str]) -> str:
        prompt = f"""
You are {self.name}, an independent expert.

Answer the question using ONLY the context.
If unsure, say "I don't know".

Context:
{context}

Question:
{query}
"""

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt}
        ).json()

        return res["response"]
