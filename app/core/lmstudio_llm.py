from openai import OpenAI
from typing import List, Dict
from .base_llm import BaseLLM
from .config import LMSTUDIO_BASE_URL, LMSTUDIO_MODEL, DEFAULT_TEMPERATURE
from .logging import log_debug
#update
from app.core.json_utils import safe_parse_json
from app.schemas.task_response import TaskResponse
from pydantic import ValidationError

class LMStudioClient(BaseLLM):

    def __init__(self):
        self.client = OpenAI(
            base_url=LMSTUDIO_BASE_URL,
            api_key="lm-studio"  # dummy key required
        )

    def chat(self, messages: List[Dict], temperature: float = DEFAULT_TEMPERATURE) -> str:
        log_debug("Sending request to LM Studio")

        response = self.client.chat.completions.create(
            model=LMSTUDIO_MODEL,
            messages=messages,
            temperature=temperature
        )

        return response.choices[0].message.content
    
    def structured_chat(self, messages, schema, temperature=0.2, max_retries=3):
        for attempt in range(max_retries):

            response = self.chat(messages, temperature=temperature)

            try:
                parsed = safe_parse_json(response)
                validated = schema.model_validate(parsed)
                return validated

            except (ValueError, ValidationError) as e:
                print(f"Retry {attempt+1}: Invalid structured output → {e}")

                messages.append({
                    "role": "system",
                    "content": "Your previous response was invalid. Return ONLY valid JSON."
                })

        raise Exception("Failed to produce valid structured output after retries.")

    