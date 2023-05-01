from lib.core.game_manager.map.unit import Unit, Move


class GuiUnit(Unit):
    def __init__(self, coordinates, location):
        Unit.__init__(self, location)

        self.coordinates = coordinates

class GuiMove(Move):
    def __init__(self, unit, province_target, target_coordinates):
        Move.__init__(self, unit, province_target)

        self.target_coordinates = target_coordinates
