from src.common.exceptions import NegativeArgumentException
from src.simulation import run_simulation


def main() -> None:
    """
    Пользователь вводит число шагов и сид, с которым будет запущенна симуляция.
    :return: Данная функция ничего не возвращает
    """
    try:
        steps = int(input("Введите количество шагов симуляции: "))
    except ValueError:
        print("Значение должно быть целым числом")
        return
    try:
        seed = input("Введите сид, либо 'None' при его отсутствии: ")
        if seed == "None":
            seed = None
        else:
            seed = int(seed)
    except ValueError:
        print("Значение должно быть целым числом")
        return
    try:
        run_simulation(steps=steps, seed=seed)
    except NegativeArgumentException:
        print("Значение должно быть неотрицательным числом")
        return


if __name__ == "__main__":
    # Проверка ошибки №2
    # from src.objects.goose import Goose
    # print(Goose("Ваня") == Goose("Ваня"))

    # Проверка ошибки №3
    from src.containers.goose_collection import GooseCollection
    from src.containers.player_collection import PlayerCollection

    # from src.objects.player import Player
    # gooses = GooseCollection()
    # players = PlayerCollection()
    # print(gooses)
    # print(players)
    # players.append(Player("Федя"))
    # print(players)
    # print(gooses)

    main()
