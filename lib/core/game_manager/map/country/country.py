from ..province import *


class Country:
    def __init__(self, name: str, provinces: list):
        
        # Type checking
        if type(name) != str:
            raise TypeError("The first argument has the wrong type")
        if type(provinces) != list:
            raise TypeError("The second argument has the wrong type")

        # Need to check the type in the list
        for pr in provinces:
            if not issubclass(type(pr), Province):
                raise TypeError("The second argument has the wrong type")
            elif pr.province_type == ProvinceType.water.value:
                raise ValueError("A water province cannot belong to a country's territory")
                

        self.name = name
        self.provinces = set(provinces)
        self.stability = 0

        self.units = set()
