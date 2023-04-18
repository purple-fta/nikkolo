from ..province import *


class Unit:
    """Unit. Pawn on the map

        Args:
            location (Province): The province in which the unit is located
    """
    def __init__(self, location: Province):
        # Type checking
        if not issubclass(type(location), Province):
            raise TypeError("The first argument has the wrong type")
        
        self.location = location
        self.power = 1
        self.protection = 1


class Move:
    def __init__(self, unit: Unit, province_target: Province):

        # Type checking
        if not issubclass(type(unit), Unit):
            raise TypeError("The first argument has the wrong type")
        if not issubclass(type(province_target), Province):
            raise TypeError("The second argument has the wrong type")

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
