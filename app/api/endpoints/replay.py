from fastapi import APIRouter, Query, Depends, HTTPException
from app.db.session import get_db
from app.db.models import TranscriptSegment
from app.services.tts_service import TTSService
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/")
async def replay_audio(id: str = Query(..., description="transcript_segments id to replay"), db: Session = Depends(get_db)):
    transcript_segment = db.query(TranscriptSegment).filter(TranscriptSegment.id == id).first()
    if not transcript_segment:
        raise HTTPException(status_code=404, detail="No transcript segment found for id={id}")

    result = TTSService().generate_speech(transcript_segment.text, f"replay_{id}")
    return {"file_path": f"{result}"}