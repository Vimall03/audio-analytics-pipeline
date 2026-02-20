from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from app.core.config import settings
from typing import Generator

DATABASE_URL = getattr(settings, "DATABASE_URL", None)
if not DATABASE_URL:
	raise RuntimeError("DATABASE_URL is not set in settings.")

engine: Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
