import pytest
from pytest_mock import MockerFixture

from src.containers.chip_collection import ChipCollection
from src.containers.player_collection import PlayerCollection
from src.objects.casino import Casino
from src.objects.chip import Chip
from src.objects.player import Player


def test_player_collection():
    chips10 = ChipCollection([Chip(10)])
    chips100 = ChipCollection([Chip(100)])
    players = PlayerCollection([Player("Федя", balance=chips10)])
    assert len(players) == 1
    players += Player("Не Федя", balance=chips100)
    assert len(players) == 2
    assert players.count == 110
    assert players.min_balance == 10
    assert players.players_names == ["Федя", "Не Федя"]
    players -= 50
    assert len(players) == 1
    assert players[0].balance.count == 50
    players += 10
    assert players[0].balance.count == 60
    players.disco()


def test_player_collection_type_error():
    chips = ChipCollection([Chip(10)])
    players = PlayerCollection()
    players.append(Player("Самир", chips))
    with pytest.raises(TypeError):
        players.append(1)
    with pytest.raises(TypeError):
        players.append(Chip(10))
    with pytest.raises(TypeError):
        players += "abcaba"
    with pytest.raises(TypeError):
        players -= "abcaba"


def test_player_collection_play_pocker(caplog, mocker: MockerFixture):
    players = PlayerCollection([Player("Андрей"), Player("Федя")])
    casino = Casino(players)
    mocker.patch("src.objects.casino.randint", return_value=2)
    casino.play_pocker()
    assert players.count == 200
    assert players.min_balance == 98
    assert "покер" in caplog.text
