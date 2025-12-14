from copy import deepcopy
from typing import Generic, TypeVar, Iterator

from src.common.config import logger
from src.models.collection import Collection

K = TypeVar('K')
V = TypeVar('V')


class DictEntity(Collection, Generic[K, V]):
    def __init__(self, data: dict[K, V] = None) -> None:
        if data is None:
            data = {}
        self.data = data

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[tuple[K, V]]:
        return iter(self.data.items())

    def __getitem__(self, key: K) -> V:
        if key not in self.data:
            raise KeyError(f"Ключа {key} нет в {self.data}")
        return self.data[key]

    def __setitem__(self, key: K, value: V) -> None:
        if key not in self.data:
            logger.debug(f"Добавлен {key}: {value}")
            self.data[key] = value
        else:
            logger.debug(f"Изменение {key}: {self.data[key]} -> {value}")
            self.data[key] = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __contains__(self, item: K) -> bool:
        return item in self.data

    def __delitem__(self, key: K) -> None:
        if key not in self.data:
            raise KeyError(f"Ключа {key} нет в {self.data}")
        logger.debug(f"Удален элемент {key}: {self.data[key]}")
        del self.data[key]
