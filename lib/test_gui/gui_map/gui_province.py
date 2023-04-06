from ...core import *


class GuiProvince(Province):
    def __init__(self, name: str, province_type: ProvinceType, coordinates, is_supply_center: bool):
        Province.__init__(self, name, province_type, is_supply_center)
        self.coordinates = coordinates