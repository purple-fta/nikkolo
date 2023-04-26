from lib.core.game_manager import Province, ProvinceType


class GuiProvince(Province):
    def __init__(self, name, province_type, is_supply_center, tiles_coordinates):
        Province.__init__(self, name, province_type, is_supply_center)

        self.tiles_coordinates = tiles_coordinates
        