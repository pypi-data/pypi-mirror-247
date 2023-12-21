from abc import ABC, abstractmethod
from typing import Any

class Player(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def receive_prompt(self, prompt: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def generate_reply(self) -> Any:
        raise NotImplementedError