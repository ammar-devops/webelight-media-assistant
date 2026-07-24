from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.core.database import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(String, unique=True, nullable=False)

    filename = Column(String)

    status = Column(String)

    progress = Column(Integer, default=0)

    video_path = Column(Text)

    audio_path = Column(Text)

    transcript = Column(Text)

    summary = Column(Text)

    translation = Column(Text)

    language = Column(String)

    duration = Column(String)

    error = Column(Text)

    created_at = Column(String)

    updated_at = Column(String)