from random import random

from src._collections.chip_collection import ChipCollection
from src.common.config import logger
from src.objects.chip import Chip
from src.models.game_entity import GameEntity


class Player(GameEntity):
    def __init__(self, name: str, balance: ChipCollection = ChipCollection([Chip(100)])):
        super().__init__(name, balance)

    def __repr__(self) -> str:
        return f"Player({self.name}, balance={self.balance})"

    def __add__(self, other):
        if isinstance(other, int):
            return Player(self.name, self.balance + other)
        if isinstance(other, Chip):
            return Player(self.name, self.balance + other.count)
        raise TypeError

    def __sub__(self, other):
        if isinstance(other, int):
            self.balance -= other
            return self
        if isinstance(other, Chip):
            self.balance -= other.count
            return self
        raise TypeError

    def spin(self, bet: int | Chip) -> None:
        if isinstance(bet, int):
            bet = Chip(bet)
        logger.info(f"Игрок {self.name} делает ставку {bet} фишек")
        if random() < 0.4:
            self.balance += bet
            logger.info(f"Игрок {self.name} смог выйграть в борьбе за {bet} фишек в нечестном казино")
        else:
            # try:
            # TODO перенести это в класс Casino
            self.balance -= bet
            # except NotEnoughChipsException:
            #     logger.info(
            #         f"Игрок {self.name} депнул всё в казино и слил. Не получилось не фартануло, пацан к успеху шёл")
            #     return
            logger.info(f"Игрок {self.name} с треском слил {bet} фишек")
