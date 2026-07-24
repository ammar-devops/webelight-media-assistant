from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.job_service import get_job

router = APIRouter(tags=["Summary"])


class SummaryRequest(BaseModel):

    job_id: str


@router.post("/")
def summary(
    request: SummaryRequest,
    db: Session = Depends(get_db),
):

    job = get_job(
        db,
        request.job_id,
    )

    if job is None:

        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "success": True,
        "summary": job.summary,
    }