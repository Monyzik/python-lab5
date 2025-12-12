from src.common.exceptions import NotEnoughChipsException
from src.models.list_entity import ListEntity
from src.objects.chip import Chip


class ChipCollection(ListEntity[Chip]):
    expected_type = Chip

    def __add__(self, other) -> "ChipCollection":
        if isinstance(other, ChipCollection):
            return ChipCollection(self.data + other.data)
        if isinstance(other, int):
            self.append(Chip(other))
            return ChipCollection(self.data)
        if isinstance(other, Chip):
            self.append(other)
            return ChipCollection(self.data)
        raise TypeError

    def __sub__(self, other) -> "ChipCollection":
        if isinstance(other, ChipCollection) or isinstance(other, Chip):
            other = other.count
        if isinstance(other, int):
            while not self.is_empty() and self.back().count <= other:
                other -= self.pop().count
            if self.is_empty():
                raise NotEnoughChipsException(self.__sub__)
            self.back().count -= other
            return ChipCollection(self.data)
        raise TypeError

    @property
    def count(self) -> int:
        result = 0
        for chip in self:
            result += chip.count
        return result

    def trade_to_one_chip(self) -> "ChipCollection":
        one_chip = Chip(self.count)
        self.clear()
        self.append(one_chip)
        return self
