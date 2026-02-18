from pydantic import BaseModel
from typing import Dict, Any

class ToolCall(BaseModel):
    thought: str
    tool_name: str
    arguments: Dict[str, Any]