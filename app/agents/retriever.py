
from app.memory.vectore_store import VectorStore


class RetreiverAgent:
    def __init__(self):
        self.store = VectorStore()
        self.store.load()

    def retrieve(self, query:str, top_k:int):
        return self.store.search(query, k=top_k)