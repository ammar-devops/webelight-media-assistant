from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.job_service import get_job
from app.services.job_service import get_jobs

router = APIRouter(tags=["Jobs"])


@router.get("")
def jobs(db: Session = Depends(get_db)):

    return get_jobs(db)


@router.get("/{job_id}")
def job(job_id: str, db: Session = Depends(get_db)):

    result = get_job(db, job_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return result