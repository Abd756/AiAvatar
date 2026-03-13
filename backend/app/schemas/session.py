from pydantic import BaseModel, Field

class BrainResponse(BaseModel):
    action: str = Field(description="The action to take: NEXT, REASK, ACKNOWLEDGE, or CLOSE")
    avatar_response: str = Field(description="The verbal response for the avatar to speak")
    thought_process: str = Field(description="Brief internal reasoning for this decision")
