import os
from app.core.celery_app import celery
from app.services.stt_service import STTService
from app.services.coach_service import CoachService
from app.db.session import SessionLocal
from app.db.models import Call, TranscriptSegment

@celery.task(bind=True, name="process_audio_task", max_retries=0) # Set to 0 for DX, Will be adjusted for production.
def process_audio(self, file_path, call_id):

    db = SessionLocal()
    try:
        call_record = db.query(Call).filter(Call.id == call_id).first()
        
        print(f"Starting transcription for Call {call_id} at {file_path}")

        response = STTService().transcribe_audio(file_path)
        print(f"Deepgram Response for Call {call_id}: {response}")

        results = response.results
        channels = results.channels
        if not channels:
            raise ValueError("No channels in Deepgram response")

        alternatives = channels[0].alternatives
        if not alternatives:
            raise ValueError("No alternatives in Deepgram response")

        utterances = results.utterances or []
        if not utterances:
            raise ValueError("No utterances returned from Deepgram")

        print(utterances)

        segments_to_add = []
        # 3. Process each segment individually
        for utt in utterances:
            text = utt.transcript
            speaker = f"Speaker {utt.speaker}"
            start = utt.start
            end = utt.end

            # Temporary assignmet for sentiment and coachability
            # Ideally will be calling the CoachService ()
            sentiment = "neutral"
            is_coachable = False

            segments_to_add.append(
                TranscriptSegment(
                    call_id=call_id,
                    speaker_tag=speaker,
                    text=text,
                    start_time=start,
                    end_time=end,
                    sentiment=sentiment,
                    is_coachable=is_coachable
                )
            )

        # 4. Bulk Insert for Efficiency
        db.add_all(segments_to_add)

        # 5. Update in the status  db
        call_record.status = "completed"
        db.commit()

        return {"status": "success", "segments_processed": len(segments_to_add)}

    except Exception as exc:
        db.rollback()
        print(f"Error processing call {call_id}: {exc}")
        # Retry logic for transient errors (CELERY LEVEL)
        raise self.retry(exc=exc, countdown=30)
    finally:
        db.close()
        if os.path.exists(file_path):
            os.remove(file_path)
