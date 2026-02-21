
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	DATABASE_URL: str = ""  # Will be read from .env
	UPLOAD_DIR: str = "uploads"
	CELERY_BROKER_URL: str = ""
	CELERY_RESULT_BACKEND: str = ""
	DEEPGRAM_API_KEY: str = ""

	class Config:
		env_file = ".env"

settings = Settings()
