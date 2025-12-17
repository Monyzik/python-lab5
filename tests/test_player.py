import pytest
from pytest_mock import MockerFixture

from src.containers.chip_collection import ChipCollection
from src.containers.player_collection import PlayerCollection
from src.objects.chip import Chip
from src.objects.goose import Goose
from src.objects.player import Player
from src.objects.casino import Casino


def test_player(caplog):
    player = Player("Федя")
    assert "Федя" in player.__repr__()
    player()
    assert "Федя:" in caplog.text
    player += 100
    assert player.balance.count == 200
    player -= 100
    assert player.balance.count == 100
    player = player + Chip(100)
    assert player.balance.count == 200
    player = player - Chip(100)
    assert player.balance.count == 100


def test_type_error():
    player = Player("Федя")
    with pytest.raises(TypeError):
        player += Player("Не Федя")
    with pytest.raises(TypeError):
        player -= Player("Не Федя")


def test_player_spin(caplog, mocker: MockerFixture):
    player = Player("Андрей")
    casino = Casino(PlayerCollection([player]))
    mocker.patch("src.objects.casino.randint", return_value=100)
    mocker.patch("src.objects.player.random", return_value=0.2)
    casino.spin()
    assert player.balance.count == 200
    mocker.patch("src.objects.casino.randint", return_value=200)
    mocker.patch("src.objects.player.random", return_value=0.7)
    casino.spin()
    assert player.full_name not in casino.casino_balances
    assert "Игрок Андрей делает ставку" in caplog.text


def test_comparison():
    a = Goose(name="", balance=ChipCollection([Chip(10), Chip(20)]))
    b = Player(name="", balance=ChipCollection([Chip(20), Chip(20)]))
    assert (a == b) == False
    assert (a < b) == True
    assert (a <= b) == True
    assert (a > b) == False
    assert (a >= b) == False
    with pytest.raises(TypeError):
        print(a < 1)
    with pytest.raises(TypeError):
        print(a <= 1)
    with pytest.raises(TypeError):
        print(a == 1)
