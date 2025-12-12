import copy
from typing import Generic, TypeVar, Iterator

from src.common.config import logger
from src.models.collection import Collection

K = TypeVar('K')
V = TypeVar('V')


class DictEntity(Collection, Generic[K, V]):
    def __init__(self, data: dict[K, V] = None) -> None:
        if data is None:
            data = {}
        self.data = copy.deepcopy(data)

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[tuple[K, V]]:
        return iter(self.data.items())

    def __getitem__(self, key: K) -> V:
        if key not in self.data:
            raise KeyError(f"Ключа {key} нет в {self.data}")
        return self.data[key]

    def __setitem__(self, key: K, value: V) -> None:
        logger.debug(f"Изменение {key}: {self.data[key]} -> {value}")
        self.data[key] = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __delitem__(self, key):
        if key not in self.data:
            raise KeyError(f"Ключа {key} нет в {self.data}")
        logger.debug(f"Удален элемент {self.data[key]}")
        del self.data[key]
