import json
import re
from typing import Any

def extract_json(text: str) -> str:
    """
    Extract the first JSON object found in text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response")

    return match.group()

def safe_parse_json(text: str) -> Any:
    json_str = extract_json(text)
    return json.loads(json_str)