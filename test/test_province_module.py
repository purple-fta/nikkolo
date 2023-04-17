from lib.core.game_manager.map.province import Province, ProvinceType

import pytest


def test_create_province():
    assert Province("123", ProvinceType.land.value, True)

    with pytest.raises(ValueError):
        assert Province([123], ProvinceType.land.value, True)

        assert Province("123", ProvinceType().land.value, True)
        assert Province("123", ProvinceType().land, True)
        assert Province("123", ProvinceType.land, True)
        assert Province("123", 1, True)
        assert Province("123", "123", True)
        assert Province("123", [1], True)
        assert Province("123", 10000, True)
        
        assert Province("123", ProvinceType.land.value, "123")
