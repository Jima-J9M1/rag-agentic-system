import requests
import json

LLM_MODEL = "llama3"

class CriticAgent:
    def critique(self, query: str, answers: list[str], context: list[str]) -> dict:
        prompt = f"""
You are a critical reviewer.

Given:
- The question
- Multiple answers
- The reference context

Identify:
- Which answers are unsupported
- Where answers disagree
- Any hallucinations

Respond ONLY in JSON:
- issues: list
- best_candidate_index: integer
- explanation: string

Context:
{context}

Question:
{query}

Answers:
{answers}
"""

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "format": "json"}
        ).json()

        return json.loads(res["response"])
