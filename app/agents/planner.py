import json
import requests


LLM_MODEL = "llama3"

class PlannerAgent:

    def plan(self, query:str):
        prompt =  f"""
        You are a planning agent.

        Given the user's query, decide:
         1. Does this require document retrieval?
         2. How many documents to retrieve? (1 - 5)

         Respond ONLY in JSON.


         Query:
         {query}

         response format:
         {{
            "needs_retrieval": "yes" | "no",
            "top_k": 1-5
         }}
        """

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model":LLM_MODEL,
                "prompt":prompt,
                "format":"json",
                "stream":False
            }
        ).json()

        return json.loads(res['response']) 