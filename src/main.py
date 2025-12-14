from src._collections.chip_collection import ChipCollection
from src.objects.chip import Chip
from src.objects.goose import Goose
from src.objects.player import Player
from src.simulation import run_simulation


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    run_simulation(seed=13121, steps=30)


if __name__ == "__main__":
    # players = PlayerCollection([Player("1"), Player("2"), Player("3")])
    #
    # # print(players)
    # goose = HonkGoose("Петя")
    # casino = CasinoBalances({goose.name: goose.balance, players[0].name: players[0].balance, players[1].name: players[1].balance,
    #                          players[2].name: players[2].balance})
    # players[0].spin(100)
    # del casino[players[0].name]
    # casino.print_rating()
    # goose.superpower(players)
    # # print(players)
    # casino.print_rating()

    # a = Goose(name="", balance=ChipCollection([Chip(10), Chip(20)]))
    # b = Player(name="", balance=ChipCollection([Chip(20), Chip(20)]))
    # print(a == b)
    # print(a < b)
    # print(a <= b)
    # print(a > b)
    # print(a >= b)
    main()
