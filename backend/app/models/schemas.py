from pydantic import BaseModel
from typing import Optional


class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    filename: Optional[str] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    translation: Optional[str] = None
    error: Optional[str] = None