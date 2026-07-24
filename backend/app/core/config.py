import os


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "AI Media Assistant",
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True",
    ) == "True"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///database/ai_media.db",
    )

    UPLOAD_DIR = os.getenv(
        "UPLOAD_DIR",
        "uploads",
    )

    OUTPUT_DIR = os.getenv(
        "OUTPUT_DIR",
        "output",
    )

    WHISPER_MODEL = os.getenv(
        "WHISPER_MODEL",
        "base",
    )

    WHISPER_DEVICE = os.getenv(
        "WHISPER_DEVICE",
        "cpu",
    )

    WHISPER_COMPUTE_TYPE = os.getenv(
        "WHISPER_COMPUTE_TYPE",
        "int8",
    )

    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434",
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5:1.5b",
    )


settings = Settings()