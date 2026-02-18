from typing import Union
from .tool_call import ToolCall
from .final_answer import FinalAnswer

AgentResponse = Union[ToolCall, FinalAnswer]