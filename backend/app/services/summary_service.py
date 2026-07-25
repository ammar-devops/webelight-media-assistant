import os

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://host.docker.internal:11434",
)

MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:1.5b",
)

client = Client(host=OLLAMA_HOST)


def generate_summary(transcript: str):

    try:

        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant. "
                        "Create a short, clear summary of the transcript."
                    ),
                },
                {
                    "role": "user",
                    "content": transcript,
                },
            ],
        )

        return {
            "success": True,
            "summary": response["message"]["content"],
        }

    except Exception as e:

        return {
            "success": False,
            "summary": "",
            "error": str(e),
        }
