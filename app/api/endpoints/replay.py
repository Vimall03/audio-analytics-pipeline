from fastapi import APIRouter, Query, Depends, HTTPException
from app.db.session import get_db
from app.db.models import TranscriptSegment
from app.services.tts_service import TTSService
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import datetime

router = APIRouter()

@router.post("/")
async def replay_audio(id: str = Query(..., description="transcript_segments id to replay"), db: Session = Depends(get_db)):
  try:
    transcript_segment = db.query(TranscriptSegment).filter(TranscriptSegment.id == id).first()
    if not transcript_segment:
        raise HTTPException(status_code=404, detail="No transcript segment found for id={id}")

    file_name = f"replay_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    file_path = TTSService().generate_speech(transcript_segment.text, file_name)
    return FileResponse(file_path, media_type="audio/mpeg", filename=file_name)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error replaying segment: {e}")