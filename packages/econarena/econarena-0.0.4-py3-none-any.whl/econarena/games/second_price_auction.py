import json
import textwrap
from typing import Any, List

import numpy as np

from .game import Game


class SecondPriceAuction(Game):
    budget: int
    private_values: List[int]
    bidding_prices: List[float]
    fouls: List[bool]
    status: bool
    winner: int
    payoffs: List[float]

    def _set_rule(self) -> None:
        """Set the rules for the Second Price Auction game.

        Configures prompt and key for extraction.
        """
        self.rule_prompt = textwrap.dedent("\
            You are participating in an auction.\n\
            The basic rules are as follows:\n\
                - it consists of {} bidders, included you.\n\
                - this is a one-round auction.\n\
                - there is only 1 item, and your private value of the item is {} units(private values may vary among bidders).\n\
                - you have {} units of assets, and you need to place a bid which is not higher than your assets.\n\
                - everyone does not know either private value of others or how others would make choices beforehand.\n\
                - The bidder who places the highest bid among all the bids will get the item, and only need to pay an amount of assets equalling to the second-highest bid among all the bids.\n\
                - If there are multiple highest bid, only the bidder with minimal index by order will get the item.\n\
                - If you get the item, your payoff equals to your remaining assets(=assets deducting payment) plus your private value, otherwise your payoff equals to your original assets.\n\
                - your goal is to maximize your overall payoffs(notice that getting the item is not necessary).\n\
            \n\
            Please just strictly output a JSON string, which has following keys:\n\
                - understanding: str, your brief understanding of the auction\n\
                - choice: float, the price which you would like to place the bid at\n\
                - reason: str, the brief reason why you made the choice\n\
        ")
        self.key_to_extract = "choice"

    def __init__(self, num_players: int, budget: int = 1000, mean_private_value: int = 500,
                 std_private_value: int = 100) -> None:
        """
        Initialize the Second Price Auction instance.

        Draw random sample from a normal distribution
        and assign it to the private value of specific player.
        Args:
            num_players (int): The number of players in the game.
            budget (int, optional): The budget for each player.
            mean_private_value (int, optional): The mean value for private values.
            std_private_value (int, optional): The standard deviation for private values.
        """

        super().__init__(num_players)
        self.budget = budget
        self.private_values = []
        while len(self.private_values) < self.num_players:
            value = int(np.random.normal(mean_private_value, std_private_value))
            if 0 < value <= self.budget:
                self.private_values.append(value)
        self.bidding_prices = [np.NaN] * self.num_players
        self._set_rule()

    def get_rule(self, idx: int) -> str:
        """
        Get the rule prompt for a specific player.

        Insert the number of players, the private values of the player and
        the upper bound for choosing numbers into the rule prompt string and return.

        Args:
            idx (int): The index of the player.

        Returns:
            str: The rule prompt.
        """

        return self.rule_prompt.format(self.num_players, self.private_values[idx], self.budget)

    def extract_from_raw_reply(self, reply: str):
        """
        Extract information from the raw reply string and return the bidding price.

        Args:
            reply (str): The raw reply string.

        Returns:
            float: The bidding price.
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
        self.bidding_prices[idx] = self.extract_from_raw_reply(reply)

    def feedback_result(self, **kwarg) -> Any:
        """
        Provide feedback on the game result.

        Returns:
            dict: A dictionary containing relevant information.For
            example:

            {'budget': 1000,
            'private_values': [657, 503, 327],
            'choices': [657.0, 502.0, 600.0],
            'status': True,
            'fouls': [False, False, False],
            'winner': 0,
            'payoffs': [1057.0, 1000.0, 1000.0]}
        """
        self.fouls = [False if not np.isnan(value) and 0 <= value <= self.budget else True
                      for value in self.bidding_prices]

        count_valid = sum([1 if not br else 0
                           for br in self.fouls])
        self.status = True if count_valid >= 2 else False

        self.winner = np.nanargmax(self.bidding_prices)

        self.payoffs = [1.0 * self.budget if not self.fouls[idx] else np.NaN
                        for idx in range(self.num_players)]
        profit = (self.private_values[self.winner] - np.nanmax(np.delete(self.bidding_prices, self.winner))
                  if self.status else np.NaN
                  )
        self.payoffs[self.winner] = self.budget + profit

        result = {
            "budget": self.budget,
            "private_values": self.private_values,
            "choices": self.bidding_prices,
            "status": self.status,
            "fouls": self.fouls,
            "winner": self.winner,
            "payoffs": self.payoffs
        }
        return result
