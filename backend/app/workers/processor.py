from app.core.database import SessionLocal
from app.services.ffmpeg_service import extract_audio
from app.services.job_service import update_job
from app.services.summary_service import generate_summary
from app.services.whisper_service import transcribe_audio


def process_job(job_id: str, video_path: str):

    db = SessionLocal()

    try:

        update_job(
            db,
            job_id,
            status="extracting_audio",
            progress=20,
            video_path=video_path,
        )

        audio_path = extract_audio(video_path)

        update_job(
            db,
            job_id,
            status="transcribing",
            progress=40,
            audio_path=audio_path,
        )

        transcript = transcribe_audio(audio_path)

        if not transcript.get("success"):

            update_job(
                db,
                job_id,
                status="failed",
                progress=100,
                error=transcript.get("error", "Transcription failed"),
            )

            return

        update_job(
            db,
            job_id,
            transcript=transcript["text"],
            language=transcript.get("language"),
            duration=str(transcript.get("duration")),
            status="summarizing",
            progress=70,
        )

        summary = generate_summary(transcript["text"])

        if summary.get("success"):

            update_job(
                db,
                job_id,
                summary=summary["summary"],
                status="completed",
                progress=100,
            )

        else:

            update_job(
                db,
                job_id,
                status="failed",
                progress=100,
                error=summary.get("error", "Summary failed"),
            )

    except Exception as e:

        update_job(
            db,
            job_id,
            status="failed",
            progress=100,
            error=str(e),
        )

    finally:

        db.close()