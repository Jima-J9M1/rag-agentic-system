

import requests
from app.memory.vectore_store import VectorStore


LLM_MODEL = "llama3"

class RAGPipeline:
    def __init__(self):
        self.store = VectorStore()
        self.store.load()

    def answer(self, query:str):
        context = self.store.search(query)

        prompt = f"""
        Answer the question using ONLY the context below.
        If the answer is not in the context, say "I don't know".

        Context:
        {context}

        Question:
        {query}

        """

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model":LLM_MODEL, "prompt":prompt, "stream":False}
        ).json()

        # res = res.json()


        return res['response']


    



