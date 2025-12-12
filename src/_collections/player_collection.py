from src.common.exceptions import NotEnoughChipsException
from src.models.list_entity import ListEntity
from src.objects.player import Player


class PlayerCollection(ListEntity[Player]):
    expected_type = Player

    def __add__(self, other) -> "PlayerCollection":
        if isinstance(other, int):
            for player in self:
                player += other
        if isinstance(other, Player):
            return PlayerCollection(self.data + other)
        raise TypeError

    def __sub__(self, other) -> "PlayerCollection":
        if isinstance(other, int):
            to_delete = []
            for player in self:
                try:
                    player -= other
                except NotEnoughChipsException:
                    to_delete.append(player)
            for player in to_delete:
                self.remove(player)
            return PlayerCollection(self.data)
        raise TypeError
