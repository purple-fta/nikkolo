<<<<<<< Updated upstream
class Move:
    def __init__(self, unit, target):
        self.unit = unit
        self.target = target

class Unit:
    def __init__(self, location):
        self.location = location
=======
from ..province import *


class Unit:
    """Unit. Pawn on the map

        Args:
            location (Province): The province in which the unit is located
    """
    def __init__(self, location: Province): 
        self.location = location
        self.power = 1
        self.protection = 1


class Move:
    def __init__(self, unit: Unit, target: Province):
        self.power = unit.power
        self.unit = unit
        self.target = target


class SupportMove(Move):
    def __init__(self, unit, province_target: Province, move_target: Move):
        Move.__init__(self, unit, province_target)
        self.move_target = move_target


class SupportHold(Move):
    def __init__(self, unit, province_target: Province, unit_target: Unit):
        Move.__init__(self, unit, province_target)
        self.unit_target = unit_target
>>>>>>> Stashed changes
