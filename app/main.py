from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import integration, transcribe, speak, replay

app = FastAPI (
  title="Audio Analytics Pipeline API",
  description="API for audio analytics pipeline, including transcription, text-to-speech, and replay",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True,
)

app.include_router(transcribe.router, prefix="/transcribe", tags=["Transcription"])
app.include_router(speak.router, prefix="/speak", tags=["Text-to-Speech"])  
app.include_router(replay.router, prefix="/replay", tags=["Replay"])
app.include_router(integration.router, prefix="/integration", tags=["Integration"])

@app.get("/")
def root():
    return {
      "status": "Healthy"
    }
