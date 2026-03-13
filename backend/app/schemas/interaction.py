from pydantic import BaseModel
from typing import Optional

class InteractionInput(BaseModel):
    session_id: str
    user_input: str
    user_name: Optional[str] = None
    script_name: str = "Daily Check-In"
