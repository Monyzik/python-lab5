from src.models.list_entity import ListEntity
from src.objects.goose import Goose, WarGoose


class GooseCollection(ListEntity[Goose]):
    expected_type = Goose

    def __add__(self, other) -> "GooseCollection":
        if isinstance(other, Goose):
            self.append(other)
            return GooseCollection(self.data)
        raise TypeError

    def disco(self) -> None:
        for goose in self:
            goose()
            goose.honk()

    def evolution(self):
        for goose in self:
            if isinstance(goose, WarGoose):
                goose.damage += 1
            goose.honk_volume += 1

# gooses = GooseCollection([Goose("Петя"), Goose("Самир", honk_volume=100)])
# gooses.disco()
# print(gooses)
# # gooses.append(Player('abacaba'))
# gooses.evolution()
# del gooses[:2]
# print(gooses)
