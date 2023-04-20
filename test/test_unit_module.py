from lib.core.game_manager.map import Unit, Province, ProvinceType, \
                                      Move, SupportHold, SupportMove, \
                                      ConvoyMove, UnitType

import pytest


@pytest.mark.parametrize("location", [[1], 2, "3", True])
def test_create_unit_with_type_error(location):
    assert Unit(Province("", ProvinceType.land.value, True))

    with pytest.raises(TypeError):
        assert Unit(location)

@pytest.mark.parametrize(("unit", "target"), [ [[1],   1],
                                               ["2",  [2]],
                                               [True, "3"] ])
def test_create_move_with_type_error(unit, target):
    with pytest.raises(TypeError):
        assert Move(unit, target)

@pytest.mark.parametrize(("unit", "target", "move_target"), [ [[1],   1,  '1'],
                                                              ["2",  [2],  2 ],
                                                              [True, "3", [3]] ])
def test_create_support_move_with_type_error(unit, target, move_target):
    assert SupportMove(Unit(Province("", ProvinceType.land.value, True)), 
                       Province("", ProvinceType.land.value, True), 
                       Move(Unit(Province("", ProvinceType.land.value, True)), Province("", ProvinceType.land.value, True)))

    with pytest.raises(TypeError):
        assert SupportMove(unit, target, move_target)

@pytest.mark.parametrize(("unit", "target", "unit_target"), [ [[1],   1,  '1'],
                                                              ["2",  [2],  2 ],
                                                              [True, "3", [3]] ])
def test_create_support_hold_with_type_error(unit, target, unit_target):
    assert SupportHold(Unit(Province("", ProvinceType.land.value, True)),
                       Province("", ProvinceType.land.value, True),
                       Unit(Province("", ProvinceType.land.value, True)))
    
    with pytest.raises(TypeError):
        assert SupportHold(unit, target, unit_target)

@pytest.mark.parametrize(("unit", "province_target", "ships"), [ [[1],   1,  '1'],
                                                              ["2",  [2],  2 ],
                                                              [True, "3", [3]] ])
def test_create_convoy_with_type_error(unit, province_target, ships):
    assert ConvoyMove(Unit(Province("", ProvinceType.coast.value, True)), 
                      Province("", ProvinceType.coast.value, True),
                      [Unit(Province("", ProvinceType.water.value, True), UnitType.nautical.value),
                       Unit(Province("", ProvinceType.water.value, True), UnitType.nautical.value)])
    
    with pytest.raises(TypeError):
        assert ConvoyMove(unit, province_target, ships)

@pytest.mark.parametrize(("unit", "province_target", "ships"), [ 
    [
        Unit(Province("", ProvinceType.water.value, False)),
        Province("", ProvinceType.coast.value, False),
        [Unit(Province("", ProvinceType.water.value, False)),
         Unit(Province("", ProvinceType.water.value, False))]
    ],
    
    [
        Unit(Province("", ProvinceType.coast.value, False)), 
        Province("", ProvinceType.land.value, False), 
        [Unit(Province("", ProvinceType.water.value, False)),
         Unit(Province("", ProvinceType.water.value, False))]
    ],
    
    [
        Unit(Province("", ProvinceType.coast.value, False)), 
        Province("", ProvinceType.coast.value, False), 
        [Unit(Province("", ProvinceType.land.value, False)),
         Unit(Province("", ProvinceType.land.value, False))]
    ]])
def test_create_convoy_with_value_error(unit, province_target, ships):
    ConvoyMove(Unit(Province("", ProvinceType.coast.value, False)), 
               Province("", ProvinceType.coast.value, False), 
               [Unit(Province("", ProvinceType.water.value, False)),
                Unit(Province("", ProvinceType.water.value, False))])
    
    with pytest.raises(ValueError):
        ConvoyMove(unit, province_target, ships)
