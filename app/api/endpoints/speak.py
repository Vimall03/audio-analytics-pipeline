from fastapi import APIRouter
from app.api.schemas import SpeakRequest
from app.services.tts_service import TTSService

router = APIRouter()

@router.post("/")
async def speak_text(request: SpeakRequest):
    print(f"Received text to speak: {request.text}")
    file_path = TTSService().generate_speech(request.text, "output.mp3")
    return {f"file_path": {file_path}}