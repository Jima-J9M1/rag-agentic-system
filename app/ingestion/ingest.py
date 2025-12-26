
# This script is responsible for loading text documents from a directory, adding them to a vector store, and saving the vector store.
import os

from app.memory.vectore_store import VectorStore

def load_document(path="data/docs"):
    """
    Load all documents from the specified directory into a list.

    Args:
        path (str): The directory path to load documents from.

    Returns:
        list: List of strings, where each string is the content of a document file.
    """
    docs = []
    for fname in os.listdir(path):
        with open(os.path.join(path, fname)) as f:
            docs.append(f.read())
    # The return statement should be outside the for loop to ensure all files are processed.
    return docs

def ingest():
    """
    Loads documents and stores them in a vector store for later retrieval.
    """
    store = VectorStore()  # Assumes VectorStore is defined elsewhere and handles vector representation of documents.
    docs = load_document()
    store.add_documents(docs)
    store.save()  # Persists the vector store to disk or any other storage.

if __name__ == "__main__":
    # When this script is run directly, invoke the ingest process.
    ingest()