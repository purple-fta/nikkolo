from lib.core.game_manager.map.unit import Unit


class GuiUnit(Unit):
    def __init__(self, coordinates, location):
        Unit.__init__(self, location)

        self.coordinates = coordinates
