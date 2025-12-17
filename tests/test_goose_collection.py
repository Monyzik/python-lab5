import pytest

from src.containers.chip_collection import ChipCollection
from src.containers.goose_collection import GooseCollection
from src.objects.chip import Chip
from src.objects.goose import Goose, WarGoose


def test_goose_collection(caplog):
    gooses = GooseCollection()
    assert gooses.is_empty()
    gooses += WarGoose("Андрей")
    assert len(gooses) == 1
    assert gooses[0].name == "Андрей"
    assert gooses.back.honk_volume == 10
    gooses.evolution(10)
    assert "Эволюция гусей началась" in caplog.text
    assert gooses.back.honk_volume == 20
    assert gooses.back.damage == 20
    gooses.disco()
    assert "Андрей" in caplog.text
    assert "ГАГАГАГА" in caplog.text


def test_goose_collection_type_error():
    chips = ChipCollection([Chip(10)])
    gooses = GooseCollection()
    gooses.append(Goose("Федя", chips))
    with pytest.raises(TypeError):
        gooses.append(1)
    with pytest.raises(TypeError):
        gooses.append(Chip(10))
    with pytest.raises(TypeError):
        gooses += Chip(10)
