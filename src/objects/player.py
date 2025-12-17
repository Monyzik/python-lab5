from random import random, choice
from typing import Callable

from src.containers.casino_balance import CasinoBalances
from src.containers.chip_collection import ChipCollection
from src.common.config import logger
from src.common.constants import PLAYER_PHRASES
from src.common.exceptions import NotEnoughElementsException
from src.models.game_entity import GameEntity
from src.objects.chip import Chip


class Player(GameEntity):
    def __init__(self, name: str, balance: ChipCollection = None):
        if balance is None:
            balance = ChipCollection([Chip(100)])
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
        if isinstance(other, int) or isinstance(other, Chip):
            return Player(self.name, self.balance - other)
        raise TypeError

    def __call__(self, *args, **kwargs):
        logger.info(f"{self.full_name}: {choice(PLAYER_PHRASES)}")

    def spin(self, bet: int | Chip, casino_balances: CasinoBalances, unregister_func: Callable) -> None:
        """
        Игрок крутит рулетку.
        :param bet: Ставка, которую сделал игрок.
        :param casino_balances: Балансы всех игроков в казино.
        :param unregister_func: Функция, которая удаляет игрока, если он обанкротился.
        :return: Ничего не возвращает.
        """
        if isinstance(bet, int):
            bet = Chip(bet)
        logger.info(f"Игрок {self.name} делает ставку {bet} фишек")
        if random() <= 0.4:
            logger.info(f"Игрок {self.name} смог выйграть в борьбе за {bet} фишек в нечестном казино")
            casino_balances[self.full_name] = (self.balance + bet).count
            return
        try:
            logger.info(f"Игрок {self.name} с треском слил {bet} фишек")
            casino_balances[self.full_name] = (self.balance - bet).count
        except NotEnoughElementsException:
            unregister_func(self)
