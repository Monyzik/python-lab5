from src.common.config import logger
from src.models.list_entity import ListEntity
from src.objects.goose import Goose, WarGoose, HonkGoose


class GooseCollection(ListEntity[Goose]):
    expected_type = Goose

    def __add__(self, other) -> "GooseCollection":
        if isinstance(other, Goose):
            self.append(other)
            return GooseCollection(self.data)
        raise TypeError

    def disco(self) -> None:
        """
        Запускает диско гусей, они веселятся и издают разные звуки.
        :return: Ничего не возвращает.
        """
        for goose in self:
            goose()
            goose.honk()

    def evolution(self, power: int = 1) -> None:
        """
        Добавляет каждому гусю по power громкости, если это WarGoose, то также добавляет power единицу урона
        :param power: Значение, на которое эволюционируют гуси, по умолчанию 1
        :return: Ничего не возвращает
        """
        logger.info("Эволюция гусей началась, все гуси стали сильнее и громче")
        for goose in self:
            if isinstance(goose, WarGoose):
            # Ошибка 5. Неправильный код:
            # if isinstance(goose, HonkGoose):
                goose.damage += power
            goose.honk_volume += power
