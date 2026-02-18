from pydantic import BaseModel

class FinalAnswer(BaseModel):
    thought: str
    answer: str
    confidence: float