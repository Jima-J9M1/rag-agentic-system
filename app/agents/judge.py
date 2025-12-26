import requests

LLM_MODEL = "llama3"

class JudgeAgent:
    def decide(self, answers: list[str], critique: dict) -> str:
        index = critique.get("best_candidate_index", 0)
        return answers[index]
