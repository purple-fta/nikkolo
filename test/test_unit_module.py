from lib.core.game_manager.map import Unit, Province, ProvinceType, Move, SupportHold, SupportMove

import pytest


@pytest.mark.parametrize("location", [[1], 2, "3", True])
def test_create_unit(location):
    assert Unit(Province("", ProvinceType.land.value, True))

    with pytest.raises(TypeError):
        assert Unit(location)

@pytest.mark.parametrize(("unit", "target"), [ [[1],   1],
                                               ["2",  [2]],
                                               [True, "3"] ])
def test_create_move(unit, target):
    with pytest.raises(TypeError):
        assert Move(unit, target)

@pytest.mark.parametrize(("unit", "target", "move_target"), [ [[1],   1,  '1'],
                                                              ["2",  [2],  2 ],
                                                              [True, "3", [3]] ])
def test_create_support_move(unit, target, move_target):
    assert SupportMove(Unit(Province("", ProvinceType.land.value, True)), 
                       Province("", ProvinceType.land.value, True), 
                       Move(Unit(Province("", ProvinceType.land.value, True)), Province("", ProvinceType.land.value, True)))

    with pytest.raises(TypeError):
        assert SupportMove(unit, target, move_target)

@pytest.mark.parametrize(("unit", "target", "unit_target"), [ [[1],   1,  '1'],
                                                              ["2",  [2],  2 ],
                                                              [True, "3", [3]] ])
def test_create_support_hold(unit, target, unit_target):
    assert SupportHold(Unit(Province("", ProvinceType.land.value, True)),
                       Province("", ProvinceType.land.value, True),
                       Unit(Province("", ProvinceType.land.value, True)))
    
    with pytest.raises(TypeError):
        assert SupportHold(unit, target, unit_target)
 
