from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterator

from src.common.exceptions import EmptyCollectionException
from src.models.collection import Collection

T = TypeVar('T')
_T = TypeVar('_T')


class ListEntity(Collection, ABC, Generic[T]):
    expected_type = object

    def __init__(self, data: list[T] = None) -> None:
        if data is None:
            data = []
        for item in data:
            if not isinstance(item, self.expected_type):
                raise TypeError
        self.data = data

    # Ошибка 3. Неправильный код:
    # def __init__(self, data: list[T] = []) -> None:
    #     for item in data:
    #         if not isinstance(item, self.expected_type):
    #             raise TypeError
    #     self.data = data

    @abstractmethod
    def __add__(self, other):
        pass

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __getitem__(self, item: int | slice) -> T:
        if isinstance(item, int):
            return self.data[item]
        if isinstance(item, slice):
            return self.__class__(self.data[item])
        raise TypeError("Индекс должен быть числом или срезом")

    def __setitem__(self, key: int | slice, value) -> None:
        if isinstance(key, int) or isinstance(key, slice):
            self.data[key] = value
            return
        raise TypeError("Индекс должен быть числом или срезом")

    def __delitem__(self, key: int | slice):
        if isinstance(key, int) or isinstance(key, slice):
            del self.data[key]
            return
        raise TypeError("Индекс должен быть числом или срезом")

    def __contains__(self, item: T) -> bool:
        if not isinstance(item, self.expected_type):
            raise TypeError(f"Неправильный тип элемента, ожидаемый: {self.expected_type}")
        return item in self.data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.data})'

    def is_empty(self) -> bool:
        """
        Проверка коллекции на пустоту.
        :return: True, если коллекция пустая, иначе False.
        """
        return len(self) == 0

    def append(self, item: T) -> None:
        """
        Добавляет элемент в конец коллекции.
        :param item: Элемент, который будет добавляться.
        :return: Ничего не возвращает.
        """
        if not isinstance(item, self.expected_type):
            raise TypeError
        self.data.append(item)

    def remove(self, item: T) -> None:
        """
        Удаляет элемент из коллекции.
        :param item: Элемент, который нужно удалить.
        :return: Ничего не возвращает.
        """
        if not isinstance(item, self.expected_type):
            raise TypeError
        self.data.remove(item)

    def pop(self, index: int = None) -> T:
        """
        Удаляет элемент из коллекции по индексу.
        :param index: Индекс элемента, который будет удален.
        :return: Возвращает удаленный элемент.
        """
        if self.is_empty():
            raise EmptyCollectionException(self.pop, self.__class__)
        if index is None:
            return self.data.pop()
        return self.data.pop(index)

    def clear(self) -> None:
        """
        Очищает коллекцию.
        :return: Ничего не возвращает.
        """
        self.data.clear()

    @property
    def back(self) -> T:
        """
        :return: Возвращает последний элемент коллекции.
        """
        if self.is_empty():
            raise EmptyCollectionException(ListEntity.back, self.__class__)
        return self.data[-1]

    @back.setter
    def back(self, value: T) -> None:
        """
        Присваивает последний элемент коллекции.
        :param value: Значение, которые будет присвоено.
        :return: Ничего не возвращает.
        """
        if self.is_empty():
            raise EmptyCollectionException(ListEntity.back, self.__class__)
        self.data[-1] = value

    def get_typed_list(self, needed: type[_T]) -> "ListEntity[_T]":
        """
        Возвращает коллекцию, с элементами, которые являются наследниками класса needed.
        :param needed: Наследником какого класса будут элементы данной коллекции.
        :return: Возвращает коллекцию, с элементами, которые являются наследниками класса needed.
        """
        return self.__class__([item for item in self if isinstance(item, needed)])
