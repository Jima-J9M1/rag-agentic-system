import requests

LLM_MODEL = "llama3"

class AnswerAgent:
    def answer(self, query: str, context: list[str]) -> str:
        prompt = f"""
You are an answering agent.

Rules:
- Use ONLY the provided context
- If the answer is missing, say "I don't know"
- Do NOT use outside knowledge

Context:
{context}

Question:
{query}
"""

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "stream":False}
        ).json()

        return res["response"]
