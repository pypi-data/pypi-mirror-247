from abc import abstractmethod
from typing import Any

from .player import Player

class Agent(Player):
    api_base: str
    api_key: str
    organization: str
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.api_base = None
        self.api_key = None
        self.organization = None

    @abstractmethod
    def receive_prompt(self, prompt: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def generate_reply(self) -> Any:
        raise NotImplementedError