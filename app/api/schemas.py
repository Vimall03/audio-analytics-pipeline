from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class SpeakRequest(BaseModel):
    text: str = Field(..., example="Lets move forward with this plan.")

class CallCreateResponse(BaseModel):
    call_id: UUID
    status: str
    message: str

class SegmentSchema(BaseModel):
    speaker_tag: str
    text: str
    sentiment: str
    is_coachable: bool

    class Config:
        from_attributes = True 
