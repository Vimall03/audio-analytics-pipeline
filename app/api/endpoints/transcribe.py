from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
import uuid, shutil
from pathlib import Path
from app.core.config import settings
from app.db.models import Call
from app.worker.tasks import process_audio


UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.post("/")
async def transcribe_audio(
  file: UploadFile = File(...),
  db: Session = Depends(get_db)
):
    if file is None or file.content_type is None:
        raise HTTPException(status_code=400, detail="No file uploaded or file type could not be determined.")
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio format.")
    
    call_id = uuid.uuid4()
    extension = Path(file.filename).suffix
    internal_filename = f"{call_id}{extension}"
    file_path = UPLOAD_DIR / internal_filename


    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    new_call = Call(id=call_id, filename=internal_filename, status="processing")
    db.add(new_call)
    db.commit()
    
    # CELERY CALL HERE
    task = process_audio.apply_async(args=[str(file_path)])


    return {
        "call_id": str(call_id),
        "task_id": task.id,
        "status": "processing",
        "message": "Audio upload successful. Transcription is running in the background."
    }