
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	DATABASE_URL: str = "" # Will be read from .env
	UPLOAD_DIR: str = "uploads"

	class Config:
		env_file = ".env"

settings = Settings()
