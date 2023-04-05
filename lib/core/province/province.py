from enum import Enum


class ProvinceType(Enum):
    land = 1
    coast = 2
    water = 3


class Province:
    def __init__(self, province_type: ProvinceType, is_supply_center: bool):
        self.province_type = province_type
        self.is_supply_center = is_supply_center
