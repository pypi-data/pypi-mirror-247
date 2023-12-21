from abc import ABC, abstractmethod
from typing import Any


class Game(ABC):
    num_players: int
    rule_prompt: str
    key_to_extract: str

    def __init__(self, num_players: int, **kwargs) -> Any:
        self.num_players = num_players
        self.rule_prompt = None
        self.key_to_extract = None

    @abstractmethod
    def get_rule(self, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def make_decision(self, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def feedback_result(self, **kwarg) -> Any:
        raise NotImplementedError
