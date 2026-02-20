import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Call(Base):
    """
    Store metadata about each call, including filename, status, and creation time from /transcribe endpoint. 
    This allows us to track the processing state of each call and manage related transcript segments.
    """
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    segments = relationship("TranscriptSegment", back_populates="call", cascade="all, delete-orphan")

class TranscriptSegment(Base):
    """
    Store individual transcript segments for each call including speaker tags, text, timestamps, sentiment, and coachability.
    This allows us to analyze the content of each call in detail and provide insights based on the transcript data.
    """
    __tablename__ = "transcript_segments"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"))
    speaker_tag = Column(String)
    text = Column(String, nullable=False)
    start_time = Column(Float)
    end_time = Column(Float)
    sentiment = Column(String)
    is_coachable = Column(Boolean, default=False)
    call = relationship("Call", back_populates="segments")