from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterator

from src.common.exceptions import EmptyCollectionException
from src.models.collection import Collection

T = TypeVar('T')


class ListEntity(Collection, ABC, Generic[T]):
    expected_type = object

    def __init__(self, data: list[T] = None) -> None:
        if data is None:
            data = []
        for item in data:
            if not isinstance(item, self.expected_type):
                raise TypeError
        self.data = data

    @abstractmethod
    def __add__(self, other):
        pass

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __getitem__(self, item: int) -> T:
        if isinstance(item, int):
            return self.data[item]
        if isinstance(item, slice):
            return self.__class__(self.data[item])
        raise TypeError

    def __setitem__(self, key: int | slice, value: T):
        if isinstance(key, int) or isinstance(key, slice):
            self.data[key] = value
        raise TypeError

    def __delitem__(self, key: int | slice):
        if isinstance(key, int) or isinstance(key, slice):
            del self.data[key]
            return
        raise TypeError

    def __contains__(self, item: T) -> bool:
        if not isinstance(item, self.expected_type):
            raise TypeError
        return item in self.data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.data})'

    def is_empty(self) -> bool:
        return len(self) == 0

    def append(self, item: T) -> None:
        if not isinstance(item, self.expected_type):
            raise TypeError
        self.data.append(item)

    def remove(self, item: T) -> None:
        if not isinstance(item, self.expected_type):
            raise TypeError
        self.data.remove(item)

    def pop(self, index: int = None) -> T:
        if self.is_empty():
            raise EmptyCollectionException(self.pop, self.__class__)
        if index is None:
            return self.data.pop()
        return self.data.pop(index)

    def clear(self) -> None:
        self.data.clear()

    @property
    def back(self) -> T:
        if self.is_empty():
            raise EmptyCollectionException(self.back, self.__class__)
        return self.data[-1]

    @back.setter
    def back(self, value: T) -> None:
        self.data[-1] = value

    def get_typed_list(self, needed: type) -> "ListEntity":
        return self.__class__([item for item in self if isinstance(item, needed)])
