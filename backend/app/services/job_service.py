import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.job import Job


def create_job(db: Session, filename: str):

    job = Job(
        job_id=str(uuid.uuid4()),
        filename=filename,
        status="queued",
        progress=0,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job(db: Session, job_id: str):

    return db.query(Job).filter(Job.job_id == job_id).first()


def get_jobs(db: Session):

    return db.query(Job).order_by(Job.id.desc()).all()


def update_job(db: Session, job_id: str, **kwargs):

    job = get_job(db, job_id)

    if job is None:
        return None

    for key, value in kwargs.items():

        if hasattr(job, key):
            setattr(job, key, value)

    job.updated_at = datetime.utcnow().isoformat()

    db.commit()

    db.refresh(job)

    return job