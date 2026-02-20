from deepgram import DeepgramClient
from app.core.config import settings

class STTService:
    def __init__(self):
        self.client = DeepgramClient(api_key=settings.DEEPGRAM_API_KEY)

    def transcribe_audio(self, file_path: str):

        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        options = {
            "model": "nova-2",    
            "smart_format": True,  
            "diarize": True,      
            "utterances": True,   
            "punctuate": True     
        }

        response = self.client.listen.v1.media.transcribe_file(
            request=audio_bytes,
            **options
        )

        return response