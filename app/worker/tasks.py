import os
from app.core.celery_app import celery
from app.services.stt_service import STTService
from app.services.coach_service import CoachService
from app.db.session import SessionLocal
from app.db.models import Call, TranscriptSegment
from app.core.logger import logger

@celery.task(bind=True, name="process_audio_task", max_retries=3) # Set to 0 for DX, Will be adjusted for production.
def process_audio(self, file_path, call_id):

    db = SessionLocal()
    try:
        call_record = db.query(Call).filter(Call.id == call_id).first()
        
        logger.info(f"Starting transcription for Call {call_id} at {file_path}")


        # For testing: use a hardcoded Deepgram-like response instead of calling the API
        response = STTService().transcribe_audio(file_path)

        """
          Used the below code for testing the rest of the pipeline without making actual API calls to Deepgram
        """
        # from types import SimpleNamespace
        # response = SimpleNamespace(
        #     results=SimpleNamespace(
        #         channels=[
        #             SimpleNamespace(
        #                 alternatives=[
        #                     SimpleNamespace(
        #                         transcript='The stale smell of old beer lingers. It takes heat to bring out the odor. A cold dip restores health and zest. A salt pickle tastes fine with ham. Tacos al pastor are my favorite. A zestful food is the hot cross bun.',
        #                         confidence=0.9992107,
        #                         words=[],
        #                         paragraphs=None,
        #                         summaries=None,
        #                         topics=None
        #                     )
        #                 ],
        #                 detected_language=None
        #             )
        #         ],
        #         utterances=[
        #             SimpleNamespace(transcript='The stale smell of old beer lingers.', speaker=0, start=1.12, end=3.62),
        #             SimpleNamespace(transcript='It takes heat to bring out the odor.', speaker=0, start=4.32, end=6.42),
        #             SimpleNamespace(transcript='A cold dip restores health and zest.', speaker=0, start=6.88, end=9.46),
        #             SimpleNamespace(transcript='A salt pickle tastes fine with ham. Tacos al pastor are my favorite.', speaker=0, start=9.92, end=14.55),
        #             SimpleNamespace(transcript='A zestful food is the hot cross bun.', speaker=0, start=15.01, end=17.67)
        #         ]
        #     )
        # )

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

        for utt in utterances:
            text = utt.transcript
            speaker = f"Speaker {utt.speaker}"
            start = utt.start
            end = utt.end

            
            sentiment = CoachService().analyze_sentiment(text)
            is_coachable = CoachService().is_coachable(text, sentiment, speaker)

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

        # Bulk Insert for Efficiency
        db.add_all(segments_to_add)

        # Update in the status  db
        call_record.status = "completed"
        db.commit()

        return {"status": "success", "segments_processed": len(segments_to_add)}

    except Exception as exc:
        db.rollback()
        logger.info(f"Error processing call {call_id}: {exc}")
        # Retry logic for transient errors (CELERY LEVEL)
        raise self.retry(exc=exc, countdown=30)
    finally:
        db.close()
        # if os.path.exists(file_path):
        #     os.remove(file_path)