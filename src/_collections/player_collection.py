from random import sample, randint, choice

from src.common.config import logger
from src.common.exceptions import NotEnoughElementsException, NegativeArgumentException
from src.models.list_entity import ListEntity
from src.objects.player import Player


class PlayerCollection(ListEntity[Player]):
    expected_type = Player

    def __add__(self, other) -> "PlayerCollection":
        if isinstance(other, int):
            for player in self:
                player += other
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
        ans = 0
        for player in self:
            ans += player.balance
        return ans

    @property
    def min_balance(self) -> int:
        return min(self.data).balance.count

    @property
    def players_names(self) -> list[str]:
        ans = []
        for player in self:
            ans.append(player.name)
        return ans

    def disco(self) -> None:
        for player in self:
            player()

    # def play_pocker(self, players_count: int):
    #     if players_count < 0:
    #         raise NegativeArgumentException(self.play_pocker)
    #     if players_count > len(self):
    #         raise NotEnoughElementsException(self.play_pocker)
    #
    #     players = PlayerCollection(sample(self.data, players_count))
    #     bet = randint(1, players.min_balance)
    #     logger.info(f"Игроки {', '.join(players.players_names)} играют покер, каждый поставил {bet}")
    #     winner = choice(players)
    #     logger.info(f"{winner.name} победил в покере {bet * len(players)}")
    #     winner += bet * len(players)
    #     for player in players:
    #         try:
    #             player -= bet
    #         except NotEnoughElementsException:
    #             self.remove(player)
