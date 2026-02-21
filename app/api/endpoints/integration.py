from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import TranscriptSegment, Call

router = APIRouter()

@router.get("/coachable-moments")
def get_cochable_moments(db: Session = Depends(get_db)):
    # Returns all the coachable moments from the transcript segments.
    try: 
      coachable_moments = db.query(TranscriptSegment).filter(TranscriptSegment.is_coachable == True).all()
      if not coachable_moments:
          raise HTTPException(status_code=404, detail="No coachable moments found.")
      result = [{
      "id": segment.id,
      "call_id": str(segment.call_id),
      "speaker_tag": segment.speaker_tag,
      "text": segment.text,
      "start_time": segment.start_time,
      "end_time": segment.end_time,
      "sentiment": segment.sentiment,
      "is_coachable": segment.is_coachable
      } for segment in coachable_moments]
      
      return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving coachable moments: {e}")

# Additional endpoint for dashbaord integration
@router.get("/calls")
def get_calls(db: Session = Depends(get_db)):
    # Returns all calls with their metadata.
    try:
        calls = db.query(Call).all()
        if not calls:
            raise HTTPException(status_code=404, detail="No calls found.")
        result = [{
            "id": str(call.id),
            "filename": call.filename,
            "status": call.status,
            "created_at": call.created_at.isoformat()
        } for call in calls]
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving calls: {e}")

@router.get("/transcript-segments")
def get_transcript_segments(call_id: str = Query(..., description="call id to get transcript segments"), db: Session = Depends(get_db)):
    # Returns all transcript segments for a given call_id.
    try:
        segments = db.query(TranscriptSegment).filter(TranscriptSegment.call_id == call_id).all()
        if not segments:
            raise HTTPException(status_code=404, detail=f"No transcript segments found for call_id={call_id}.")
        result = [{
            "id": segment.id,
            "speaker_tag": segment.speaker_tag,
            "text": segment.text,
            "start_time": segment.start_time,
            "end_time": segment.end_time,
            "sentiment": segment.sentiment,
            "is_coachable": segment.is_coachable
        } for segment in segments]
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving transcript segments: {e}")