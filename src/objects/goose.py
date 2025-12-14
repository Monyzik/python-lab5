from typing import override

from src._collections.chip_collection import ChipCollection
from src._collections.player_collection import PlayerCollection
from src.common.config import logger
from src.models.game_entity import GameEntity
from src.objects.player import Player


class Goose(GameEntity):
    def __init__(self, name: str, balance: ChipCollection = None, honk_volume: int = 10):
        super().__init__(name, balance)
        self.honk_volume = honk_volume

    def __call__(self, *args, **kwargs):
        logger.info("ГА" * (self.honk_volume // 5))

    def honk(self) -> None:
        s = f"Я есть гусь {self.name}"
        if self.honk_volume >= 100:
            s = s.upper()
        logger.info(s)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, honk_volume={self.honk_volume}, balance={self.balance.data})"


class WarGoose(Goose):
    def __init__(self, name: str, balance: ChipCollection = None, honk_volume: int = 10, damage: int = 10):
        super().__init__(name, balance, honk_volume)
        self.damage = damage

    def attack(self, player: Player):
        logger.info(f"Гусь {self.name} атаковал {player.name}")
        player.balance -= self.damage
        self.balance += self.damage

    def steal_chip(self, player: Player, index: int):
        logger.info(f"Гусь {self.name} атаковал {player.name}")
        chip = player.balance.pop(index)
        self.balance += chip


class HonkGoose(Goose):
    def __init__(self, name: str, balance: ChipCollection = None, honk_volume: int = 10):
        super().__init__(name, balance, honk_volume)

    @override
    def honk(self) -> None:
        logger.info(f"Я есть очень громкий гусь {self.name}")

    def superpower(self, players: PlayerCollection):
        logger.info(f"Гусь {self.name} использовал суперспособность, каждый игрок потерял {self.honk_volume} фишек")
        self.balance += self.honk_volume * len(players)
        players -= self.honk_volume
        return self
