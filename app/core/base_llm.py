from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLLM(ABC):

    @abstractmethod
    def chat(self, messages: List[Dict], temperature: float = 0.2) -> str:
        pass
    