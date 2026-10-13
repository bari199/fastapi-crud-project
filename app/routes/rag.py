
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.rag.schemas.chat import ChatRequest, ChatResponse
from app.rag.services.rag_service import answer_question
from app.security import get_current_user

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/chat", response_model=ChatResponse)
def chat_with_documents(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return answer_question(
            db=db,
            question=request.question,
            top_k=request.top_k,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
