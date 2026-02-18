from .config import LLM_PROVIDER
from .lmstudio_llm import LMStudioClient
# from .ollama_llm import OllamaClient  # future use

def get_llm():
    if LLM_PROVIDER == "lmstudio":
        return LMStudioClient()
    else:
        raise ValueError("Unsupported LLM provider")