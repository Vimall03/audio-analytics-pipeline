from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def transcribe_audio():
    return {"message": "Transcription endpoint"}