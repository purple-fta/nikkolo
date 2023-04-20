from ..province import *
from enum import Enum


class UnitType(Enum):
    overland = 1
    nautical = 2



class Unit:
    """Unit. Pawn on the map

        Args:
            location (Province): The province in which the unit is located
    """
    def __init__(self, location: Province, unit_type: UnitType = None):
        # Type checking
        if not issubclass(type(location), Province):
            raise TypeError("The first argument has the wrong type")
        
        self.location = location
        self.power = 1
        self.protection = 1

        if not unit_type:
            unit_type = UnitType.nautical.value if location.province_type == ProvinceType.water.value else UnitType.overland.value
        else:
            if unit_type == UnitType.nautical.value and location.province_type == ProvinceType.land.value:
                raise ValueError("Conflict between the type of unit and the type of province where it is located")
            if unit_type == UnitType.overland.value and location.province_type == ProvinceType.water.value:
                raise ValueError("Conflict between the type of unit and the type of province where it is located")


        self.unit_type = unit_type


class Move:
    def __init__(self, unit: Unit, province_target: Province):

        # Type checking
        if not issubclass(type(unit), Unit):
            raise TypeError("The first argument has the wrong type")
        if not issubclass(type(province_target), Province):
            raise TypeError("The second argument has the wrong type")


        if unit.unit_type == UnitType.overland.value and province_target.province_type == ProvinceType.water.value:
            raise ValueError("Overland unit cannot move to water")
        if unit.unit_type == UnitType.nautical.value and province_target.province_type == ProvinceType.land.value:
            raise ValueError("Overland unit cannot move to water")


        self.power = unit.power
        self.unit = unit
        self.province_target = province_target


class SupportMove(Move):
    def __init__(self, unit: Unit, province_target: Province, move_target: Move):
        Move.__init__(self, unit, province_target)

        if not issubclass(type(move_target), Move):
            raise TypeError("The third argument has the wrong type")

        self.move_target = move_target


class SupportHold(Move):
    def __init__(self, unit: Unit, province_target: Province, unit_target: Unit):
        Move.__init__(self, unit, province_target)

        if not issubclass(type(unit_target), Unit):
            raise TypeError("The third argument has the wrong type")
        
        self.unit_target = unit_target


class ConvoyMove(Move):
    def __init__(self, unit: Unit, province_target: Province, ships: [Unit]):
        # Type checking
        if not issubclass(type(unit), Unit):
            raise TypeError("The first argument has the wrong type")
        if not issubclass(type(province_target), Province):
            raise TypeError("The second argument has the wrong type")
        if type(ships) == list:
            for i in ships:
                if not issubclass(type(i), Unit):
                    raise TypeError("The third argument has the wrong type in list")
        else:
            raise TypeError("The third argument has the wrong type")

        # Value checking
        if unit.unit_type != UnitType.overland.value:
            raise ValueError("Unit has bad type for convoy move")
        if province_target.province_type != ProvinceType.coast.value:
            raise ValueError("Target province has bad type for convoy move")
        for ship in ships:
            if ship.unit_type != UnitType.nautical.value:
                raise ValueError("Ships has bad type in list")


        Move.__init__(self, unit, province_target)
        self.ships = ships
