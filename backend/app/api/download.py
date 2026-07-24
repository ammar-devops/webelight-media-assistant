from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.export_service import (
    create_docx,
    create_pdf,
    create_srt,
    create_txt,
)
from app.services.job_service import get_job

router = APIRouter(tags=["Download"])


def _get_completed_job(db: Session, job_id: str):

    job = get_job(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Job is not completed yet",
        )

    return job


@router.get("/txt/{job_id}")
def download_txt(
    job_id: str,
    db: Session = Depends(get_db),
):

    job = _get_completed_job(db, job_id)

    file_path = create_txt(job)

    return FileResponse(
        path=file_path,
        filename=f"{job.filename}.txt",
        media_type="text/plain",
    )


@router.get("/pdf/{job_id}")
def download_pdf(
    job_id: str,
    db: Session = Depends(get_db),
):

    job = _get_completed_job(db, job_id)

    file_path = create_pdf(job)

    return FileResponse(
        path=file_path,
        filename=f"{job.filename}.pdf",
        media_type="application/pdf",
    )


@router.get("/docx/{job_id}")
def download_docx(
    job_id: str,
    db: Session = Depends(get_db),
):

    job = _get_completed_job(db, job_id)

    file_path = create_docx(job)

    return FileResponse(
        path=file_path,
        filename=f"{job.filename}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/srt/{job_id}")
def download_srt(
    job_id: str,
    db: Session = Depends(get_db),
):

    job = _get_completed_job(db, job_id)

    file_path = create_srt(job)

    return FileResponse(
        path=file_path,
        filename=f"{job.filename}.srt",
        media_type="application/x-subrip",
    )