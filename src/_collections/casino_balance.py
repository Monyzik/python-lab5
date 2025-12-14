from copy import deepcopy

from src._collections.chip_collection import ChipCollection
from src._collections.goose_collection import GooseCollection
from src._collections.player_collection import PlayerCollection
from src.common.config import logger
from src.models.dict_entity import DictEntity


class CasinoBalances(DictEntity[str, int]):
    def print_rating(self):
        sorted_rating = sorted(self.data.items(), key=lambda item: -item[1])
        logger.info("Рейтинг казино:")
        for key, value in sorted_rating:
            if 'player' in key.lower() and value == 0:
                logger.info(f"{key}: остался у разбитого корыта без копеечки в кармане")
            else:
                logger.info(f"{key}: {value}")

    def update(self, data: PlayerCollection | GooseCollection) -> None:
        if not isinstance(data, PlayerCollection) and not isinstance(data, GooseCollection):
            raise TypeError
        for item in data:
            if item.full_name not in self or self[item.full_name] != item.balance:
                self[item.full_name] = item.balance
