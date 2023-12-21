from abc import ABC, abstractmethod
import random
from typing import Any, List

import toml

from ..games import *
from ..players import *

class Host(ABC):
    config: dict
    apis: dict
    game: Game
    num_players: int
    players: List[Player]
    def __init__(self, config: dict) -> None:
        self.config = config
        self.apis = None
    
    def set_apis(self, apis: dict) -> None:
        self.apis = apis
    
    def initialize_game(self) -> Any:
        assert self.apis is not None, "api information for LLM agents is not set"
        num_players = self.config["num_players"]
        self.num_players = int(num_players)
        players_class = self.config["players_class"]
        self.players = [eval(player_class[0])(
                            api_base=self.apis[player_class[0]].get("api_base"),
                            api_key=self.apis[player_class[0]].get("api_key"),
                            secret_key=self.apis[player_class[0]].get("secret_key"),
                            model=player_class[1]
                        ) for player_class in players_class]
        game_class = self.config["game_class"]
        self.game = eval(game_class)(
                        num_players=self.num_players
                    )

    def run_game(self) -> Any:
        print("Game started")
        self.initialize_game()
        print("Game initialized")
        for index in range(self.num_players):
            rule_prompt = self.game.get_rule(idx=index)
            self.players[index].receive_prompt(rule_prompt)
            print(f"Player #{index} is making desicion")
            reply = self.players[index].generate_reply()
            print(f"Player #{index} replied")
            self.game.make_decision(idx=index, reply=reply)
        result = self.game.feedback_result()
        return result