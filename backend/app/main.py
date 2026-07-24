from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.download import router as download_router
from app.api.job import router as job_router
from app.api.summary import router as summary_router
from app.api.translate import router as translate_router
from app.api.upload import router as upload_router

from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Media Assistant",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(job_router, prefix="/jobs", tags=["Jobs"])
app.include_router(summary_router, prefix="/summary", tags=["Summary"])
app.include_router(translate_router, prefix="/translate", tags=["Translate"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(download_router, prefix="/download", tags=["Download"])


@app.get("/")
def home():
    return {
        "message": "AI Media Assistant API",
        "version": "2.0.0",
        "status": "running",
    }