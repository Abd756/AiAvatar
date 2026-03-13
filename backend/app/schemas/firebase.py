from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TranscriptMessage(BaseModel):
    role: str # "avatar" or "user"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SessionState(BaseModel):
    session_id: str
    user_name: Optional[str] = None
    script_name: str
    current_index: int = 0
    reask_count: int = 0
    status: str = "active" # "active", "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
