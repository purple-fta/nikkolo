from lib.core.game_manager.map.province import Province, ProvinceType

import pytest


@pytest.mark.parametrize(("name", "province_type", "is_supply_center"), [ [[123], ProvinceType.land.value, True],
                                       
                                       ["123", ProvinceType.land,       True],
                                       ["123", "123",                   True],
                                       ["123", [1],                     True],
                                       
                                       ["123", ProvinceType.land.value, "123"] ])
def test_create_province(name, province_type, is_supply_center):
    with pytest.raises(TypeError):
        assert Province(name, province_type, is_supply_center)
