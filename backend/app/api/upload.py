import os
import threading

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.services.job_service import create_job
from app.workers.processor import process_job

router = APIRouter(tags=["Upload"])


@router.post("")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    try:

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(
            settings.UPLOAD_DIR,
            file.filename,
        )

        with open(file_path, "wb") as buffer:

            while True:

                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                buffer.write(chunk)

        job = create_job(
            db=db,
            filename=file.filename,
        )

        thread = threading.Thread(
            target=process_job,
            args=(
                job.job_id,
                file_path,
            ),
            daemon=True,
        )

        thread.start()

        return {
            "success": True,
            "message": "File uploaded successfully.",
            "job_id": job.job_id,
            "status": "queued",
            "progress": 0,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )