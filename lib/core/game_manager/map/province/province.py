from enum import Enum


class ProvinceType(Enum):
    land = 1
    coast = 2
    water = 3


class Province:
    def __init__(self, name: str, province_type: ProvinceType, is_supply_center: bool):
        self.str = str
        self.province_type = province_type
        self.is_supply_center = is_supply_center
        
        # In the future, if the provinces have their own protection, it may be necessary. In the meantime...
        #self.protection = 0 