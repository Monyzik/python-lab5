from src.containers.chip_collection import ChipCollection
from src.containers.goose_collection import GooseCollection
from src.containers.player_collection import PlayerCollection
from src.objects.chip import Chip
from src.objects.goose import Goose, HonkGoose, WarGoose
from src.objects.player import Player
from src.objects.casino import Casino


def test_gooses(caplog):
    goose = Goose("Федя")
    goose()
    assert "ГАГА" in caplog.text
    goose.honk()
    assert "Я есть гусь Федя" in caplog.text
    goose.honk_volume = 200
    goose.honk()
    assert "Я ЕСТЬ ГУСЬ ФЕДЯ" in caplog.text
    honk_goose = HonkGoose("Федя")
    honk_goose.honk()
    assert "Я есть очень громкий гусь Федя" in caplog.text
    assert "Федя" in goose.__repr__()


def test_war_goose_attacks(caplog):
    player = Player("Андрей")
    goose = WarGoose("Федя")
    casino = Casino(PlayerCollection([player]), GooseCollection([goose]))
    casino.goose_attack()
    assert "100 -> 90" in caplog.text
    assert casino.casino_balances[player.full_name] == 90
    goose.damage = 100
    casino.goose_attack()
    assert "Удален" in caplog.text
    assert player.full_name not in casino.casino_balances


def test_war_goose_steal_chip(caplog):
    goose = WarGoose("Федя")
    player = Player("Андроид", ChipCollection([Chip(100), Chip(200)]))
    casino = Casino(PlayerCollection([player]), GooseCollection([goose]))
    casino.steal_chip()
    assert "300 -> 200" in caplog.text or "300 -> 100" in caplog.text
    assert casino.casino_balances[player.full_name] in (100, 200)
    casino.steal_chip()
    assert "Удален" in caplog.text
    assert player.full_name not in casino.casino_balances


def test_honk_goose_superpower(caplog):
    player1 = Player("Андрей")
    player2 = Player("Не Андрей")
    goose = HonkGoose("Федя")
    casino = Casino(PlayerCollection([player1, player2]), GooseCollection([goose]))
    casino.goose_superpower()
    assert "100 -> 90" in caplog.text
    assert casino.casino_balances[player1.full_name] == 90
    assert casino.casino_balances[player2.full_name] == 90
    goose.honk_volume = 100
    casino.goose_superpower()
    assert "Удален" in caplog.text
    assert player1.full_name not in casino.casino_balances
    assert player2.full_name not in casino.casino_balances
