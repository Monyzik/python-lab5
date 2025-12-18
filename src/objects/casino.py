from random import sample, randint, choice, choices

from src.containers.casino_balance import CasinoBalances
from src.containers.goose_collection import GooseCollection
from src.containers.player_collection import PlayerCollection
from src.common.config import logger
from src.common.exceptions import NotEnoughElementsException
from src.objects.goose import Goose, HonkGoose, WarGoose
from src.objects.player import Player


class Casino:
    def __init__(self, players: PlayerCollection = None, gooses: GooseCollection = None) -> None:
        self.players = PlayerCollection()
        self.gooses = GooseCollection()
        self.casino_balances = CasinoBalances()
        if players is not None:
            for player in players:
                self.register_player(player)
        if gooses is not None:
            for goose in gooses:
                self.register_goose(goose)

    def register_player(self, player: Player) -> None:
        """
        Регистрирует игрока в казино.
        :param player: Игрок, которого необходимо зарегистрировать
        :return: Ничего не возвращает.
        """
        if not isinstance(player, Player):
            raise TypeError
        self.players.append(player)
        self.casino_balances[player.full_name] = player.balance.count

    def register_goose(self, goose: Goose) -> None:
        """
        Регистрирует гуся в казино.
        :param goose: Гусь, которого необходимо зарегистрировать
        :return: Ничего не возвращает.
        """
        if not isinstance(goose, Goose):
            raise TypeError
        self.gooses.append(goose)
        self.casino_balances[goose.full_name] = goose.balance.count

    def unregister_player(self, player: Player) -> None:
        """
        Выгоняет игрока из казино.
        :param player: Игрок, которого необходимо выгнать.
        :return: Ничего не возвращает.
        """
        logger.info(f"Игрок {player.name} депнул всё в казино и слил. "
                    f"Не получилось не фартануло, пацан к успеху шёл")
        self.players.remove(player)
        del self.casino_balances[player.full_name]

    def disco(self) -> None:
        """
        Все сущности устраивают дискотеку, также игрокам приходит подарок в виде случайного количества фишек.
        :return: Ничего не возвращает.
        """
        gift = randint(100, 1000)
        logger.info(f"Вечеринка началась, всем игрокам дарят {gift} фишек на додеп")
        for player in self.players:
            player.balance += gift
            self.casino_balances[player.full_name] += gift
        self.gooses.disco()
        self.players.disco()

    def spin(self) -> None:
        """
        Случайный игрок крутит рулетку.
        :return: Ничего не возвращает.
        """
        player = choice(self.players)
        bet = randint(1, player.balance.count)
        player.spin(bet, self.casino_balances, self.unregister_player)

    def play_pocker(self) -> None:
        """
        Случайное множество игроков (len >= 2) играют в покер.
        :return: Ничего не возвращает.
        """
        if len(self.players) < 2:
            raise NotEnoughElementsException(self.play_pocker)
        players_count = randint(2, len(self.players))
        players = PlayerCollection(sample(self.players.data, players_count))
        bet = randint(1, players.min_balance)
        players.play_pocker(bet, self.casino_balances, self.unregister_player)

    def goose_superpower(self) -> None:
        """
        Рандомный HonkGoose использует свою суперспособность.
        :return: Ничего не возвращает.
        """
        honk_gooses = self.gooses.get_typed_list(HonkGoose)
        if honk_gooses.is_empty():
            raise NotEnoughElementsException(self.goose_superpower)
        honk_goose = choice(honk_gooses)
        honk_goose.superpower(self.players, self.casino_balances, self.unregister_player)
        # Ошибка 4. Неправильный код:
        # honk_goose.superpower(self.players, self.casino_balances, self.register_player)

    def goose_attack(self) -> None:
        """
        Рандомный WarGoose атакует случайного игрока.
        :return: Ничего не возвращает.
        """
        war_gooses = self.gooses.get_typed_list(WarGoose)
        if war_gooses.is_empty():
            raise NotEnoughElementsException(self.goose_attack)
        war_goose = choice(war_gooses)
        player = choice(self.players)
        war_goose.attack(player, self.casino_balances, self.unregister_player)

    def evolution(self) -> None:
        """
        Все гуси эволюционируют.
        :return: Ничего не возвращает.
        """
        self.gooses.evolution(power=randint(1, 20))

    def steal_chip(self) -> None:
        """
        Рандомный WarGoose крадет фишку у случайного игрока.
        :return: Ничего не возвращает.
        """
        war_gooses = self.gooses.get_typed_list(WarGoose)
        if war_gooses.is_empty():
            raise NotEnoughElementsException(self.goose_attack)
        war_goose = choice(war_gooses)
        player = choice(self.players)
        war_goose.steal_chip(player, randint(1, len(player.balance)) - 1)
        if player.balance.count == 0:
            self.unregister_player(player)
        else:
            self.casino_balances[player.full_name] = player.balance.count

    def step(self) -> None:
        """
        Производит один шаг симуляции казино.
        :return: Ничего не возвращает.
        """
        actions = [self.disco, self.evolution, self.spin]
        actions_weights = [10, 10, 100]
        if len(self.players) > 1:
            actions.append(self.play_pocker)
            actions_weights.append(100)
        if not self.gooses.get_typed_list(WarGoose).is_empty():
            actions.extend([self.goose_attack, self.steal_chip])
            actions_weights.extend([100, 100])
        if not self.gooses.get_typed_list(HonkGoose).is_empty():
            actions.append(self.goose_superpower)
            actions_weights.append(100)
        try:
            event = choices(actions, weights=actions_weights, k=1)[0]
            event()
        except Exception as e:
            logger.error(e)
