from enum import Enum


class ProvinceType(Enum):
    land = 1
    coast = 2
    water = 3


class Province:
    """Province on the map

        Args:
            name (str): Province name. May repeat
            province_type (ProvinceType): Province type. Variants are defined in the ProvinceType class
            is_supply_center (bool): Does the province have a Supply Center
    """
    
    def __init__(self, name: str, province_type: ProvinceType, is_supply_center: bool):
        self.name = name
        self.province_type = province_type
        self.is_supply_center = is_supply_center
        
        # In the future, if the provinces have their own protection, it may be necessary. In the meantime...
        #self.protection = 0 