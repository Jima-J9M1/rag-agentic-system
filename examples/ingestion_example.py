"""
Document Ingestion Example

This example shows how to ingest documents into the vector store.
"""

from app.ingestion.ingest import ingest, load_document

def example_ingestion():
    """
    Example of ingesting documents into the vector store.
    
    Steps:
    1. Load documents from a directory
    2. Create embeddings for each document
    3. Store in FAISS vector index
    4. Save the index for later use
    """
    
    print("=== Document Ingestion Example ===\n")
    
    # Step 1: Load documents
    print("Step 1: Loading documents from data/docs/")
    docs = load_document("data/docs")
    print(f"Loaded {len(docs)} documents\n")
    
    # Display document previews
    for i, doc in enumerate(docs[:3], 1):  # Show first 3
        print(f"Document {i} preview:")
        print(f"  {doc[:100]}...")
        print()
    
    # Step 2: Ingest documents
    print("Step 2: Ingesting documents into vector store...")
    print("  - Creating embeddings (this may take a while)...")
    print("  - Adding to FAISS index...")
    print("  - Saving index to disk...")
    
    try:
        ingest()
        print("\n✓ Ingestion complete!")
        print("  - vector_store.index created")
        print("  - vector_store.pkl created")
    except Exception as e:
        print(f"\n✗ Error during ingestion: {e}")
        return
    
    print("\nDocuments are now searchable via the RAG pipeline!")

if __name__ == "__main__":
    example_ingestion()

