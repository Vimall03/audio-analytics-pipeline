from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import TranscriptSegment

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