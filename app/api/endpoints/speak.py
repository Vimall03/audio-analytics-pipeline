from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.api.schemas import SpeakRequest
from app.services.tts_service import TTSService
import datetime
router = APIRouter()

@router.post("/")
async def speak_text(request: SpeakRequest):
    print(f"Received text to speak: {request.text}")
    file_name = f"putput_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    file_path = TTSService().generate_speech(request.text, file_name)
    return FileResponse(file_path, media_type="audio/mpeg", filename=file_name)