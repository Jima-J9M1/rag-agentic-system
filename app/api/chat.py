
from fastapi import APIRouter

from app.models.Query import QueryRequest, QueryResponse
from app.orchestration.controller import AgentController
from app.rag.pipeline import RAGPipeline


router = APIRouter()
rag = RAGPipeline()
controller = AgentController()


@router.post("/chat")
async def chat(request: QueryRequest):
    return controller.run(request.query, request.session_id)