# This file defines a VectorStore class for storing, searching, and managing document embeddings using FAISS and an external embedding model API.

import pickle        # For saving and loading Python objects to and from disk
import faiss         # Facebook AI Similarity Search library, for efficient vector similarity search
import numpy as np   # For numerical operations and arrays
import requests      # For calling the remote embedding service via HTTP

# The name of the embedding model to use when requesting embeddings from the API
EMBEDDING_MODEL = "nomic-embed-text"

class VectorStore:
    """
    VectorStore uses a FAISS index to store document embeddings and supports adding, searching, saving,
    and loading documents and their embeddings.
    """
    def __init__(self, dim=768):
        """
        Initializes the vector store.

        Args:
            dim (int): The dimension of the embeddings expected (default: 768).
        """
        self.index = faiss.IndexFlatL2(dim) # Flat L2 distance index for efficient similarity search
        self.text = []                      # Stores the raw documents' text

    def embed(self, text):
        """
        Gets an embedding vector for the provided text by querying the embedding model API.

        Args:
            text (str): Text to embed.

        Returns:
            np.ndarray: The embedding vector as a numpy array (float32).
        """
        res = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model":EMBEDDING_MODEL, "prompt":text}
        ).json()  # Calls the API and parses the JSON response

        return np.array(res['embedding'], dtype=np.float32)  # Converts to numpy array

    def add_documents(self, docs):
        """
        Embeds and adds a list of documents into the FAISS index and stores their raw text.

        Args:
            docs (list): List of documents (strings) to add.
        """
        for doc in docs:
            embedding = self.embed(doc)                    # Get embedding for the document
            self.index.add(np.array([embedding]))          # Add embedding to the FAISS index
            self.text.append(doc)                          # Store the original text

    def search(self, query, k=5):
        """
        Searches for the top-k documents most similar to the query.

        Args:
            query (str): Input query to search for similar documents.
            k (int): Number of top results to retrieve (default: 5).

        Returns:
            list: List of the most similar document texts.
        """
        embedding = self.embed(query)                                    # Get embedding for query
        distances, indices = self.index.search(np.array([embedding]), k) # Search in FAISS index
        print(indices, query, self.text)

        # what if the text is empty?
        if len(self.text) == 0:
            return []

        return [self.text[i] for i in indices[0] ]                        # Map indices to documents

    def save(self):
        """
        Saves the FAISS index and the list of document texts to disk for persistence.
        """
        faiss.write_index(self.index, "vector_store.index")
        with open("vector_store.pkl", "wb") as f:
            pickle.dump(self.text, f)

    def load(self):
        """
        Loads the FAISS index and the list of document texts from disk.
        """
        self.index = faiss.read_index("vector_store.index")
        with open("vector_store.pkl", "rb") as f:
            self.text = pickle.load(f)
