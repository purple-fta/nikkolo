from lib.core.game_manager import Country


class GuiCountry(Country):
    def __init__(self, name, provinces, color):
        Country.__init__(self, name, provinces)

        self.color = color