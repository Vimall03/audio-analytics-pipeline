import os
from gtts import gTTS
from pathlib import Path
from app.core.config import settings
from app.core.logger import logger
class TTSService:
    def __init__(self):
        self.output_dir = Path(settings.UPLOAD_DIR) / "tts_outputs" # save in tts folder for better organzation
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_speech(self, text: str, filename: str) -> str:
        """
        Converts text to speech and saves it as an mp3.
        Returns the path of the mp3 file.
        """
        try:
          # I decided to go with Google tts for faster generations, dont have to rely on celery + polling 
          # This returns the actual file in the API response ranther than a presigned URL, 
          # which is better for DX but might need to be re-evaluated for production based on file sizes and performance
            tts = gTTS(text=text, lang='en', slow=False) 
            file_path = self.output_dir / f"{filename}.mp3"
            tts.save(str(file_path))
            return str(file_path)
        except Exception as e:
            logger.error(f"TTS Generation Error: {e}")
            raise e