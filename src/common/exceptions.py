from typing import Callable


class EmptyCollectionException(Exception):
    def __init__(self, func: Callable, cls):
        super().__init__(f"Невозможно применить функцию {func.__name__} в пустом {cls.__name__}")


class NotEnoughElementsException(Exception):
    def __init__(self, func: Callable):
        super().__init__(f"Недостаточно элементов для выполнения операции: {func.__name__}")


class NegativeArgumentException(Exception):
    def __init__(self, func: Callable):
        super().__init__(f"Невозможно выполнить функцию {func.__name__} с отрицательным аргументом")
