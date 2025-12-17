from collections.abc import Callable
from random import sample, randint, choice

from src.containers.casino_balance import CasinoBalances
from src.common.config import logger
from src.common.exceptions import NotEnoughElementsException, NegativeArgumentException
from src.models.list_entity import ListEntity
from src.objects.chip import Chip
from src.objects.player import Player


class PlayerCollection(ListEntity[Player]):
    expected_type = Player

    def __add__(self, other) -> "PlayerCollection":
        if isinstance(other, int):
            for player in self:
                player += other
            return PlayerCollection(self.data)
        if isinstance(other, Player):
            self.append(other)
            return PlayerCollection(self.data)
        raise TypeError

    def __sub__(self, other) -> "PlayerCollection":
        if isinstance(other, int):
            to_delete = []
            for player in self:
                try:
                    player -= other
                except NotEnoughElementsException:
                    to_delete.append(player)
            for player in to_delete:
                logger.info(
                    f"Игрок {player.name} депнул всё в казино и слил. Не получилось не фартануло, пацан к успеху шёл")
                self.remove(player)
            return PlayerCollection(self.data)
        raise TypeError

    @property
    def count(self) -> int:
        """
        :return: Возвращает сумму балансов всех игроков.
        """
        ans = 0
        for player in self:
            ans += player.balance.count
        return ans

    @property
    def min_balance(self) -> int:
        """
        :return: Возвращает минимальный баланс всех игроков.
        """
        return min(self.data).balance.count

    @property
    def players_names(self) -> list[str]:
        """
        :return: Возвращает массив всех имён игроков.
        """
        ans = []
        for player in self:
            ans.append(player.name)
        return ans

    def disco(self) -> None:
        """
        Запускает дискотеку у игроков, они веселятся и разговаривают.
        :return: Ничего не возвращает.
        """
        for player in self:
            player()

    def play_pocker(self, bet: int | Chip, casino_balances: CasinoBalances, unregister_func: Callable) -> None:
        """
        Все игроки играют в покер на bet фишек.
        :param bet: Ставка, который сделал каждый игрок.
        :param casino_balances: Балансы всех игроков в казино.
        :param unregister_func: Функция, которая удаляет игрока, если он обанкротился.
        :return: Ничего не возвращает.
        """
        if isinstance(bet, Chip):
            bet = bet.count
        logger.info(f"Игроки {', '.join(self.players_names)} играют покер, каждый поставил {bet}")
        winner = choice(self)
        logger.info(f"{winner.name} победил в покере {bet * len(self)}")
        winner += bet * len(self)
        to_delete = []
        for player in self:
            try:
                player.balance -= bet
                casino_balances[player.full_name] = player.balance.count
            except NotEnoughElementsException:
                to_delete.append(player)
        for player in to_delete:
            unregister_func(player)
