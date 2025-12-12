from src._collections.casino_balance import CasinoBalances
from src._collections.goose_collection import GooseCollection
from src._collections.player_collection import PlayerCollection


class Casino:
    def __init__(self, players: PlayerCollection, gooses: GooseCollection) -> None:
        self.players = players
        self.gooses = gooses
        self.casino_balances = CasinoBalances()
        for collection in [players, gooses]:
            for item in collection:
                self.casino_balances[item.name] = item.balance
        print(self.casino_balances)
