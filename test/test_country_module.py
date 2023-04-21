from lib.core.game_manager.map import *

import pytest


pr1 = Province("PR1", ProvinceType.water.value, False)
pr2 = Province("PR2", ProvinceType.coast.value, False)
pr3 = Province("PR3", ProvinceType.land.value,  False)
pr4 = Province("PR4", ProvinceType.coast.value, False)
pr5 = Province("PR5", ProvinceType.water.value, False)


@pytest.mark.parametrize(("name", "provinces"), ( [1123, [pr2, pr3, pr4]],
                                                  ["12", [1, 2, 3]],
                                                  ["12", [1, pr2, 3]] ))
def test_create_country_with_type_error(name, provinces):
    with pytest.raises(TypeError):
        Country(name, provinces)

@pytest.mark.parametrize(("name", "provinces"), ( ["12", [pr2, pr5]],
                                                  ["12", [pr2, pr1]] ))
def test_create_country_with_value_error(name, provinces):
    with pytest.raises(ValueError):
        Country(name, provinces)

