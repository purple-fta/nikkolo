from lib.core.game_manager.map import Unit, Province, ProvinceType, Move, SupportHold, SupportMove

import pytest


@pytest.mark.parametrize("location", [[1], 2, "3", True])
def test_create_unit(location):
    assert Unit(Province("", ProvinceType.land.value, True))

    with pytest.raises(TypeError):
        assert Unit(location)

def test_create_move():
    assert Move(Unit(Province("", ProvinceType.land.value, True)), Province("", ProvinceType.land.value, True))

    with pytest.raises(TypeError):
        assert Move([1], 1)
        assert Move("2", [2])
        assert Move(True, "3")

def test_create_support_move():
    assert SupportMove(Move(Unit(Province("", ProvinceType.land.value, True)), Province("", ProvinceType.land.value, True)), 
                       Province("", ProvinceType.land.value, True), 
                       Move(Unit(Province("", ProvinceType.land.value, True)), Province("", ProvinceType.land.value, True)))

    with pytest.raises(TypeError):
        assert SupportMove([1], 1, '1')
        assert SupportMove("2", [2], 2)
        assert SupportMove(True, "3", [3])

def test_create_support_hold():
    assert SupportHold(Unit(Province("", ProvinceType.land.value, True)),
                       Province("", ProvinceType.land.value, True),
                       Unit(Province("", ProvinceType.land.value, True)))
    
    with pytest.raises(TypeError):
        assert SupportHold([1], 1, '1')
        assert SupportHold("2", [2], 2)
        assert SupportHold(True, "3", [3])
 
