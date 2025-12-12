from src._collections.casino_balance import CasinoBalances
from src._collections.player_collection import PlayerCollection
from src.objects.goose import HonkGoose
from src.objects.player import Player
from src.simulation import run_simulation


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    run_simulation()


if __name__ == "__main__":
    players = PlayerCollection([Player("1"), Player("2"), Player("3")])

    # print(players)
    goose = HonkGoose("Петя")
    casino = CasinoBalances({goose.name: goose.balance, players[0].name: players[0].balance, players[1].name: players[1].balance,
                             players[2].name: players[2].balance})
    players[0].spin(100)
    del casino[players[0].name]
    casino.print_rating()
    goose.superpower(players)
    # print(players)
    casino.print_rating()
    main()
