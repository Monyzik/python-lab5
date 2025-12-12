from src._collections.chip_collection import ChipCollection
from src.common.config import logger
from src.models.dict_entity import DictEntity


class CasinoBalances(DictEntity[str, ChipCollection]):
    def print_rating(self):
        sorted_rating = sorted(self.data.items(), key=lambda item: -item[1].count)
        for key, value in sorted_rating:
            logger.info(f"{key}: {value.count}")
