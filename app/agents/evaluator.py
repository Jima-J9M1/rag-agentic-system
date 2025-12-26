
import json
from app.rag.pipeline import LLM_MODEL
import requests

LLM_MODEL = "llama3"

class EvaluatorAgent:
    def evaluate(self, query:str, context:list[str], answer:str):
        prompt = f"""
        You are a evaluator agent.

        Given:
          - A user question
          - An answer 
          - The context used to generate the answer

        Evaluate:
        1. Is the answer grounded in the context?
        2. Does the answer introduce unsupported facts?
        3. Give a confidence score from 0 to 1.


        Response ONLY in JSON with fields:
         - grounded: true/false
         - hallucination_risk: low/medium/high
         - confidence: number between 0 and 1
         - explanation: short reason

         Context:
         {context}

         Question:
         {query}

         Answer:
         {answer}
        """

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model":LLM_MODEL,
                "prompt":prompt,
                "stream":False,
                "format":"json"
            }
        ).json()

        return json.loads(res['response'])