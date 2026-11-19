from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import engine
from models import Document
from schemas import AIAnalysisResponse, AgentAskRequest, AgentAskResponse
from services.agent_service import ask_agent
from services.gemini_service import GeminiServiceError, analyze_document

router = APIRouter(tags=["AI"])


@router.post("/documents/{document_id}/analyze", response_model=AIAnalysisResponse, summary="Analyze a document with Gemini")
def analyze(document_id: int):
    with Session(engine) as db:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        content = document.content

    try:
        result = analyze_document(content)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    with Session(engine) as db:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        document.ai_summary = result["summary"]
        db.commit()

    return result


@router.post("/agent/ask", response_model=AgentAskResponse, summary="Ask the read-only document agent")
def agent_ask(payload: AgentAskRequest):
    try:
        answer = ask_agent(payload.message)
        return {"answer": answer}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
