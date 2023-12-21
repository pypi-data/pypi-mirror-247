import json
import textwrap
from typing import Any, List

import numpy as np

from .game import Game


class BeautyContest(Game):
    upper_bound: int
    prize: int
    chosen_numbers: List[float]
    fouls: List[bool]
    status: bool
    winners: List[int]
    payoffs: List[float]

    def _set_rule(self) -> None:
        """Set the rules for the Beauty Contest game.

        Configures prompt and key for extraction.
        """
        self.rule_prompt = textwrap.dedent("\
            You are playing a game.\n\
            The basic rules are as follows:\n\
                - it consists of {} players, including you.\n\
                - this is a one-round game.\n\
                - you need to choose a real number between 0 and {}, 0 and {} inclusive.\n\
                - everyone does not know how others would make choices beforehand.\n\
                - the winner is the person whose number is the closest to the two thirds of the average of all chosen numbers.\n\
                - the winner gets a fixed prize, in case of a tie the prize is split amongst those who tie.\n\
                - your goal is primarily to maximize the possibility of getting the prize and secondly to maximize the your prize.\n\
            \n\
            Please just strictly output a JSON string, which has following keys:\n\
                - understanding: str, your brief understanding of the game\n\
                - choice: float, the number which you would like to choose\n\
                - reason: str, the brief reason why you made the choice\n\
        ")
        self.key_to_extract = "choice"

    def __init__(self, num_players: int, upper_bound: int = 100, prize: int = 1) -> None:
        """
        Initialize the BeautyContest instance.

        Args:
            num_players (int): The number of players in the game.
            upper_bound (int, optional): The upper bound for choosing numbers.
            prize (int, optional): The fixed prize for the winner.
        """
        super().__init__(num_players)
        self.upper_bound = upper_bound
        self.prize = prize
        self.chosen_numbers = [np.NaN] * self.num_players
        self._set_rule()

    def get_rule(self, idx: int) -> str:
        """
        Get the rule prompt for a specific player index after formatting.

        Insert the number of players and the upper bound for choosing numbers
        into the rule prompt string and return.

        Args:
            idx (int): The index of the player.

        Returns:
            str: The rule prompt after formatting.
        """
        return self.rule_prompt.format(self.num_players, self.upper_bound, self.upper_bound)

    def extract_from_raw_reply(self, reply: str):
        """
        Extract information from the raw reply string and return the choosing score.

        Args:
            reply (str): The raw reply string.

        Returns:
            float: The choosing score.
        """
        try:
            pos_fr, pos_to = reply.find("{"), reply.rfind("}")
            json_content = reply[pos_fr: pos_to + 1]
            reply_d = json.loads(json_content)
            reply_key = float(reply_d[self.key_to_extract])
        except Exception:
            return np.NaN
        return reply_key

    def make_decision(self, idx: int, reply: str) -> None:
        """
        Make a decision for a player based on their reply.

        Args:
            idx (int): The index of the player.
            reply (str): The player's reply.
        """
        self.chosen_numbers[idx] = self.extract_from_raw_reply(reply)

    def feedback_result(self, **kwarg) -> Any:
        """
        Provide feedback on the game result.

        Returns:
            dict: A dictionary containing relevant information.For
            example:

            {'upper_bound': 100,
             'choices': [0.0, 33.33, 33.33],
             'status': True,
             'fouls': [False, False, False],
             'winners': [0],
             'payoffs': [1.0, 0.0, 0.0]}
        """
        self.fouls = [False if not np.isnan(value) and 0 <= value <= self.upper_bound else True
                      for value in self.chosen_numbers]

        count_valid = sum([1 if not br else 0
                           for br in self.fouls])
        self.status = True if count_valid >= 1 else False

        avg = np.nanmean(self.chosen_numbers)
        ctr = avg * 2 / 3
        dif = [abs(val - ctr) if not self.fouls[idx] else np.NaN
               for (idx, val) in enumerate(self.chosen_numbers)]
        self.winners = list(np.where(dif == np.nanmin(dif))[0])

        self.payoffs = [0.0 if not self.fouls[idx] else np.NaN
                        for idx in range(self.num_players)]
        for winner in self.winners:
            self.payoffs[winner] = 1.0 * self.prize / len(self.winners)

        result = {
            "upper_bound": self.upper_bound,
            "choices": self.chosen_numbers,
            "status": self.status,
            "fouls": self.fouls,
            "winners": self.winners,
            "payoffs": self.payoffs
        }
        return result
