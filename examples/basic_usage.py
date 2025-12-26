"""
Basic usage example for the RAG Knowledge Assistant API.

This example demonstrates how to interact with the API using Python requests.
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BASE_URL}/chat"

def chat(query: str, session_id: str = "example-session"):
    """
    Send a query to the RAG Knowledge Assistant.
    
    Args:
        query: The question to ask
        session_id: Unique session identifier for conversation context
    
    Returns:
        dict: Response containing answer, status, and evaluation
    """
    payload = {
        "query": query,
        "session_id": session_id
    }
    
    response = requests.post(CHAT_ENDPOINT, json=payload)
    response.raise_for_status()
    
    return response.json()

def main():
    """Example usage of the chat function."""
    
    print("=== RAG Knowledge Assistant - Basic Usage Example ===\n")
    
    # Example 1: Simple query
    print("Example 1: Simple Query")
    print("-" * 50)
    result = chat("What is retrieval-augmented generation?")
    print(f"Status: {result.get('status')}")
    print(f"Answer: {result.get('answer')}")
    print(f"Confidence: {result.get('evaluation', {}).get('confidence', 'N/A')}")
    print()
    
    # Example 2: Follow-up question in same session
    print("Example 2: Follow-up Question (Same Session)")
    print("-" * 50)
    session = "conversation-1"
    result1 = chat("What is FAISS?", session_id=session)
    print(f"Q1: What is FAISS?")
    print(f"A1: {result1.get('answer')[:100]}...")
    print()
    
    result2 = chat("How does it work?", session_id=session)
    print(f"Q2: How does it work?")
    print(f"A2: {result2.get('answer')[:100]}...")
    print()
    
    # Example 3: Check evaluation details
    print("Example 3: Evaluation Details")
    print("-" * 50)
    result = chat("Explain vector embeddings")
    evaluation = result.get('evaluation', {})
    print(f"Grounded: {evaluation.get('grounded')}")
    print(f"Confidence: {evaluation.get('confidence')}")
    print(f"Full evaluation: {json.dumps(evaluation, indent=2)}")
    print()

if __name__ == "__main__":
    main()

