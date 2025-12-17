from abc import ABC, abstractmethod

from src.containers.chip_collection import ChipCollection


class GameEntity(ABC):
    def __init__(self, name: str, balance: ChipCollection = None) -> None:
        if balance is None:
            balance = ChipCollection()
        self.name = name
        self.balance = balance

    def __eq__(self, other):
        if isinstance(other, GameEntity):
            return self.name == other.name and self.balance == other.balance
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, GameEntity):
            if self.balance == other.balance:
                return self.name < other.name
            return self.balance < other.balance
        raise TypeError

    def __le__(self, other):
        if isinstance(other, GameEntity):
            if self.balance == other.balance:
                return self.name <= other.name
            return self.balance <= other.balance
        raise TypeError

    @property
    def full_name(self):
        """
        :return: Возвращает полное имя класса, вида: '{class} {name}'.
        """
        return self.__class__.__name__ + ' ' + self.name

    @abstractmethod
    def __repr__(self) -> str:
        pass
