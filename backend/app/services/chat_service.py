import requests

from app.core.config import settings


def ask_question(
    transcript: str,
    question: str,
):

    prompt = f"""
You are an AI Media Assistant.

Answer ONLY using the transcript below.

If the answer is not present in the transcript,
reply exactly:

I couldn't find that information in the transcript.

Transcript:

{transcript}

Question:

{question}
"""

    try:

        response = requests.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "answer": data.get("response", "").strip(),
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
        }