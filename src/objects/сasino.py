from copy import deepcopy
from random import sample, randint, choice, choices, random

from src._collections.casino_balance import CasinoBalances
from src._collections.goose_collection import GooseCollection
from src._collections.player_collection import PlayerCollection
from src.common.config import logger
from src.common.exceptions import NotEnoughElementsException, EmptyCollectionException
from src.objects.goose import Goose, WarGoose, HonkGoose
from src.objects.player import Player


class Casino:
    def __init__(self, players: PlayerCollection = None, gooses: GooseCollection = None) -> None:
        if players is None:
            players = PlayerCollection()
        self.players = players
        if gooses is None:
            gooses = GooseCollection()
        self.gooses = gooses
        self.casino_balances = CasinoBalances()
        for collection in [players, gooses]:
            for item in collection:
                self.casino_balances[item.full_name] = item.balance.count

    def update(self):
        self.casino_balances.update(self.players)
        self.casino_balances.update(self.gooses)

    def register_player(self, player: Player) -> None:
        if not isinstance(player, Player):
            raise TypeError
        self.players.append(player)
        self.casino_balances[player.full_name] = player.balance.count

    def register_goose(self, goose: Goose) -> None:
        if not isinstance(goose, Goose):
            raise TypeError
        self.gooses.append(goose)
        self.casino_balances[goose.full_name] = goose.balance.count

    def unregister_player(self, player: Player) -> None:
        logger.info(f"Игрок {player.name} депнул всё в казино и слил. "
                    f"Не получилось не фартануло, пацан к успеху шёл")
        self.players.remove(player)
        del self.casino_balances[player.full_name]

    def disco(self):
        logger.info("Вечеринка началась")
        self.gooses.disco()
        self.players.disco()

    def spin(self) -> None:
        player = choice(self.players)
        bet = randint(1, player.balance.count)
        logger.info(f"Игрок {player.name} делает ставку {bet} фишек")
        if random() <= 0.4:
            logger.info(f"Игрок {player.name} смог выйграть в борьбе за {bet} фишек в нечестном казино")
            self.casino_balances[player.full_name] = (player.balance + bet).count
            return
        if player.balance.count - bet > 0:
            logger.info(f"Игрок {player.name} с треском слил {bet} фишек")
            self.casino_balances[player.full_name] = (player.balance - bet).count
        else:
            self.unregister_player(player)
        # try:
        #     logger.info(f"Игрок {player.name} делает ставку {bet} фишек")
        #     if random() <= 0.4:
        #         player.balance += bet
        #         logger.info(f"Игрок {player.name} смог выйграть в борьбе за {bet} фишек в нечестном казино")
        #     else:
        #         player.balance -= bet
        #         logger.info(f"Игрок {player.name} с треском слил {bet} фишек")
        #     self.update()
        # except NotEnoughElementsException:
        #     logger.info(
        #         f"Игрок {player.name} депнул всё в казино и слил. Не получилось не фартануло, пацан к успеху шёл")
        #     self.players.remove(player)
        #     del self.casino_balances[player.full_name]

    def play_pocker(self) -> None:
        if len(self.players) < 2:
            raise NotEnoughElementsException(self.play_pocker)
        players_count = randint(2, len(self.players))
        players = PlayerCollection(sample(self.players.data, players_count))
        bet = randint(1, players.min_balance)
        logger.info(f"Игроки {', '.join(players.players_names)} играют покер, каждый поставил {bet}")
        winner = choice(players)
        logger.info(f"{winner.name} победил в покере {bet * len(players)}")
        winner += bet * len(players)
        for player in players:
            try:
                player.balance -= bet
                self.casino_balances[player.full_name] = player.balance.count
            except NotEnoughElementsException:
                self.unregister_player(player)
        # self.players.play_pocker(players_count)
        # self.update()

    def goose_superpower(self):
        honk_gooses = self.gooses.get_typed_list(HonkGoose)
        if honk_gooses.is_empty():
            raise NotEnoughElementsException(self.goose_superpower)
        # honk_goose = choice(honk_gooses)

        # honk_goose.balance += honk_goose.honk_volume * len(self.players)
        # self.players -= honk_goose.honk_volume
        honk_goose: HonkGoose = choice(honk_gooses)
        logger.info(f"Гусь {honk_goose.name} использовал суперспособность, "
                    f"каждый игрок потерял {honk_goose.honk_volume} фишек")
        for player in self.players:
            try:
                player.balance -= honk_goose.honk_volume
                self.casino_balances[player.full_name] = player.balance.count
            except NotEnoughElementsException:
                self.unregister_player(player)
        # honk_goose.superpower(self.players)
        # self.update()

    def step(self):
        actions = [self.disco, self.spin, self.goose_superpower]
        actions_weights = [1, 100, 100]
        if len(self.players) > 1:
            actions.append(self.play_pocker)
            actions_weights.append(100)
        try:
            event = choices(actions, weights=actions_weights, k=1)[0]
            event()
        except Exception as e:
            logger.error(e)
