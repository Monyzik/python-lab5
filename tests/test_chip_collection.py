import pytest

from src.containers.chip_collection import ChipCollection
from src.common.exceptions import EmptyCollectionException
from src.objects.chip import Chip


def test_chip_collection():
    lst = ChipCollection()
    lst.append(Chip(10))
    assert lst.back == 10
    lst.back = 1
    assert lst.back == 1
    assert len(lst) == 1
    assert lst.pop() == 1
    assert lst.is_empty() == True
    for _ in range(10):
        lst.append(Chip(10))
    assert len(lst) == 10
    del lst[:2]
    assert len(lst) == 8
    lst += Chip(20)
    assert lst.back == 20
    lst += ChipCollection([Chip(10)])
    assert lst.back == 10
    assert lst[-2:] == ChipCollection([Chip(20), Chip(10)])
    lst[0:2] = ChipCollection([Chip(50), Chip(20)])
    assert lst[1] == Chip(20)
    assert lst[0] == Chip(50)
    assert Chip(50) in lst
    lst.clear()
    assert lst.is_empty()


def test_ch_bad_type_exception():
    chips = ChipCollection()
    chips.append(Chip(10))
    with pytest.raises(TypeError):
        chips.append(1)
    with pytest.raises(TypeError):
        chips.append("lsnjbvhjs")
    with pytest.raises(TypeError):
        chips.append("lsnjbvhjs")
    with pytest.raises(TypeError):
        print(chips == "abacaba")
    with pytest.raises(TypeError):
        print(chips <= "abacaba")
    with pytest.raises(TypeError):
        print(chips < "abacaba")
    with pytest.raises(TypeError):
        chips += 'abacaba'
    with pytest.raises(TypeError):
        chips -= 'abacaba'
    with pytest.raises(TypeError):
        ChipCollection("abacaba")
    with pytest.raises(TypeError):
        chips["abacaba"]


def test_collection_empty_exception():
    lst = ChipCollection()
    with pytest.raises(EmptyCollectionException):
        lst.back = 0
    with pytest.raises(EmptyCollectionException):
        print(lst.back)
    with pytest.raises(EmptyCollectionException):
        lst.pop()
