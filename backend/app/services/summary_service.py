import os

import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")


def generate_summary(transcript: str):
    try:
        response = ollama.chat(
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

        summary = response["message"]["content"]

        return {
            "success": True,
            "summary": summary,
        }

    except Exception as e:
        return {
            "success": False,
            "summary": "",
            "error": str(e),
        }