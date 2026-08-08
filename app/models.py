from pydantic import BaseModel
from typing import Optional, List

class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[dict] = None   # present only on the first call
    message: Optional[str] = None      # present on every call after

class Feedback(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    next: List[str]

class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[Feedback] = None