from typing import override, Callable

from src.containers.casino_balance import CasinoBalances
from src.containers.chip_collection import ChipCollection
from src.containers.player_collection import PlayerCollection
from src.common.config import logger
from src.common.exceptions import NotEnoughElementsException
from src.models.game_entity import GameEntity
from src.objects.player import Player


class Goose(GameEntity):
    def __init__(self, name: str, balance: ChipCollection = None, honk_volume: int = 10):
        super().__init__(name, balance)
        self.honk_volume = honk_volume

    def __call__(self, *args, **kwargs) -> None:
        logger.info("ГА" * (self.honk_volume // 5))

    def honk(self) -> None:
        """
        Гусь кричит, его крик зависит от его громкости.
        :return: Ничего не возвращает
        """
        s = f"Я есть гусь {self.name}"
        if self.honk_volume >= 100:
            s = s.upper()
        logger.info(s)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, honk_volume={self.honk_volume}, balance={self.balance.data})"


class WarGoose(Goose):
    def __init__(self, name: str, balance: ChipCollection = None, honk_volume: int = 10, damage: int = 10):
        super().__init__(name, balance, honk_volume)
        self.damage = damage

    def attack(self, player: Player, casino_balances: CasinoBalances, unregister_func: Callable) -> None:
        """
        Гусь атакует игрока
        :param player: Игрок, которого атакует гусь
        :param casino_balances: Балансы всех игроков в казино.
        :param unregister_func: Функция, которая удаляет игрока, если он обанкротился.
        :return: Ничего не возвращает
        """
        logger.info(f"Гусь {self.name} атаковал {player.name}")
        try:
            player.balance -= self.damage
            casino_balances[player.full_name] -= self.damage
        except NotEnoughElementsException:
            unregister_func(player)
        self.balance += self.damage
        casino_balances[self.full_name] += self.damage

    def steal_chip(self, player: Player, index: int) -> None:
        """
        Крадет одну фишку index у игрока.
        :param player: Игрок, у которого будет украдена фишка.
        :param index: Индекс фишки, которая будет украдена.
        :return: Ничего не возвращает.
        """
        logger.info(f"Гусь {self.name} атаковал {player.name}")
        chip = player.balance.pop(index)
        self.balance += chip


class HonkGoose(Goose):
    def __init__(self, name: str, balance: ChipCollection = None, honk_volume: int = 10) -> None:
        super().__init__(name, balance, honk_volume)

    @override
    def honk(self) -> None:
        logger.info(f"Я есть очень громкий гусь {self.name}")

    def superpower(self, players: PlayerCollection, casino_balances: CasinoBalances, unregister_func: Callable) -> None:
        """
        Применяет суперспособность громкого гуся, забирая у каждого игрока honk_volume фишек.
        :param players: Список игроков, на которых действует суперспособность.
        :param casino_balances: Балансы всех игроков в казино.
        :param unregister_func: Функция, которая удаляет игрока, если он обанкротился.
        :return: Ничего не возвращает
        """
        logger.info(f"Гусь {self.name} использовал суперспособность, "
                    f"каждый игрок потерял {self.honk_volume} фишек")

        to_delete = []
        for player in players:
            try:
                player.balance -= self.honk_volume
                casino_balances[player.full_name] = player.balance.count
            except NotEnoughElementsException:
                to_delete.append(player)
        for player in to_delete:
            unregister_func(player)

        # Ошибка 1. Неправильный код:
        # for player in players:
        #     try:
        #         player.balance -= self.honk_volume
        #         casino_balances[player.full_name] = player.balance.count
        #     except NotEnoughElementsException:
        #         unregister_func(player)

        self.balance += self.honk_volume * len(players)
        casino_balances[self.full_name] = self.balance.count
