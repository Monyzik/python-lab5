from typing import Callable


class EmptyCollectionException(Exception):
    def __init__(self, func: Callable, cls):
        super().__init__(f"Невозможно применить функцию {func.__name__} в пустом {cls.__name__}")


class NotEnoughChipsException(Exception):
    def __init__(self, func: Callable):
        super().__init__(f"Недостаточно фишек для выполнения операции: {func.__name__}")
