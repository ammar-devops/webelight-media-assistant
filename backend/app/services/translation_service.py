import requests

from app.core.config import settings


def translate_text(
    text: str,
    target_language: str = "Hindi",
) -> dict:
    """
    Translate transcript using Ollama.
    """

    prompt = f"""
You are an expert translator.

Translate the following text into {target_language}.

Only return the translated text.

Text:

{text}
"""

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:

        response = requests.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        result = response.json()

        return {
            "success": True,
            "translation": result.get("response", "").strip(),
            "language": target_language,
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
        }