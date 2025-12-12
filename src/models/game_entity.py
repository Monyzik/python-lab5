import copy
from abc import ABC, abstractmethod

from src._collections.chip_collection import ChipCollection


class GameEntity(ABC):
    def __init__(self, name: str, balance: ChipCollection = None) -> None:
        if balance is None:
            balance = ChipCollection()
        self.name = name
        self.balance = copy.deepcopy(balance)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, GameEntity):
            return self.name == other.name and self.balance == other.balance
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, GameEntity):
            if self.balance.count == other.balance.count:
                return self.name < other.name
            return self.balance.count < other.balance.count
        raise TypeError

    def __ge__(self, other):
        if isinstance(other, GameEntity):
            if self.balance.count == other.balance.count:
                return self.name > other.name
            return self.balance.count > other.balance.count
        raise TypeError

    @abstractmethod
    def __repr__(self) -> str:
        pass
