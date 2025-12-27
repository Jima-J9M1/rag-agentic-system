#!/bin/bash

# RAG Knowledge Assistant - cURL Examples
# Make sure the API server is running: uvicorn app.main:app --reload

BASE_URL="http://localhost:8000"
CHAT_ENDPOINT="${BASE_URL}/chat"

echo "=== RAG Knowledge Assistant - cURL Examples ==="
echo ""

# Example 1: Simple query
echo "Example 1: Simple Query"
echo "----------------------"
curl -X POST "${CHAT_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is RAG?",
    "session_id": "curl-example-1"
  }' | jq '.'
echo ""
echo ""

# Example 2: Query requiring retrieval
echo "Example 2: Query Requiring Retrieval"
echo "-------------------------------------"
curl -X POST "${CHAT_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain how vector embeddings work in detail",
    "session_id": "curl-example-2"
  }' | jq '.'
echo ""
echo ""

# Example 3: Follow-up question (same session)
echo "Example 3: Follow-up Question"
echo "-----------------------------"
SESSION_ID="curl-conversation-1"

# First question
echo "First question:"
curl -X POST "${CHAT_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"What is FAISS?\",
    \"session_id\": \"${SESSION_ID}\"
  }" | jq '.answer'
echo ""

# Follow-up question
echo "Follow-up question:"
curl -X POST "${CHAT_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"How does it compare to other vector databases?\",
    \"session_id\": \"${SESSION_ID}\"
  }" | jq '.answer'
echo ""
echo ""

# Example 4: Check API health (Swagger docs)
echo "Example 4: Access API Documentation"
echo "-------------------------------------"
echo "Swagger UI: ${BASE_URL}/docs"
echo "ReDoc: ${BASE_URL}/redoc"
echo ""


