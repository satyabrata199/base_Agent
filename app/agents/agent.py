from app.schemas.agent_response import AgentResponse
from app.schemas.tool_call import ToolCall
from app.schemas.final_answer import FinalAnswer

class Agent:
    def __init__(self, llm, tools: dict, max_iterations: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations
        self.messages = []

    def run(self, user_input: str):
        self.messages = self._build_initial_messages(user_input)

        for _ in range(self.max_iterations):
            response = self.llm.structured_chat(
                messages=self.messages,
                schema=AgentResponse
            )

            if isinstance(response, ToolCall):
                self._handle_tool_call(response)
                continue

            if isinstance(response, FinalAnswer):
                return response

        raise Exception("Max iterations exceeded")
    def _handle_tool_call(self, tool_call: ToolCall):
        tool = self.tools.get(tool_call.tool_name)

        # CASE 1 — Tool does not exist
        if not tool:
            self.messages.append({
                "role": "system",
                "content": (
                    f"Error: Tool '{tool_call.tool_name}' does not exist. "
                    f"Available tools: {list(self.tools.keys())}. "
                    f"Use exact tool names."
                )
            })
            return

        # CASE 2 — Tool exists, execute safely
        try:
            result = tool.run(**tool_call.arguments)
        except TypeError as e:
            self.messages.append({
                "role": "system",
                "content": (
                    f"Tool argument error: {str(e)}. "
                    f"Use correct argument format."
                )
            })
            return

        # Log tool call
        self.messages.append({
            "role": "assistant",
            "content": tool_call.model_dump_json()
        })

        # Add tool result
        self.messages.append({
            "role": "tool",
            "content": str(result)
        })

    def _build_initial_messages(self, user_input: str):
        tool_names = ", ".join(self.tools.keys())

        tool_descriptions = "\n".join(
            [f"- {tool.name}(expression: str): {tool.description}"
            for tool in self.tools.values()]
        )

        system_prompt = f"""
You are an AI agent that can use tools.

IMPORTANT RULES:
- You MUST use ONLY the exact tool names listed below.
- Do NOT invent new tool names.
- If solving math, you MUST use tool_name exactly as "calculator".
- You MUST provide argument key exactly as "expression".
- Do NOT use "numbers", "values", or other keys.

Available tools:
{tool_descriptions}

When using a tool, return JSON EXACTLY matching this structure:
{{
  "thought": "...",
  "tool_name": "<one of: {tool_names}>",
  "arguments": {{...}}
}}

When giving the final answer, return JSON EXACTLY matching:
{{
  "thought": "...",
  "answer": "...",
  "confidence": 0-1
}}
"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]