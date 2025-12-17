import pytest

from src.containers.casino_balance import CasinoBalances


def test_casino_balances(caplog):
    casino_balances = CasinoBalances({"abacaba": 200})
    casino_balances["ababa"] = 100
    casino_balances.print_rating()
    assert "abacaba: 200" in caplog.text
    assert "ababa: 100" in caplog.text
    assert "baaaba" not in casino_balances
    assert "CasinoBalances" in casino_balances.__repr__()


def test_casino_balances_key_error(caplog):
    casino_balances = CasinoBalances({"ababa": 200})
    with pytest.raises(KeyError):
        print(casino_balances["abacaba"])
    with pytest.raises(KeyError):
        del casino_balances["abacaba"]
