from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.chat_service import ask_question
from app.services.job_service import get_job

router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    job_id: str
    question: str


@router.get("/")
def health():
    return {
        "success": True,
        "message": "Chat API Running"
    }


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    job = get_job(db, request.job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if not job.transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript not available",
        )

    result = ask_question(
        transcript=job.transcript,
        question=request.question,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"],
        )

    return {
        "success": True,
        "job_id": request.job_id,
        "question": request.question,
        "answer": result["answer"],
    }