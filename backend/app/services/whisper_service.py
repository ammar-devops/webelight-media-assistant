from faster_whisper import WhisperModel
from app.core.config import settings

# Load model only when first needed
_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading Faster-Whisper model...")

        _model = WhisperModel(
            settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE,
        )

        print("Whisper model loaded successfully.")

    return _model


def transcribe_audio(audio_path: str):
    """
    Transcribe an audio file using Faster-Whisper.

    Args:
        audio_path (str): Path to audio file

    Returns:
        dict: transcription result
    """

    model = get_model()

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True,
    )

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return {
        "success": True,
        "language": info.language,
        "duration": info.duration,
        "text": transcript.strip(),
    }