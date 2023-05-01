from .gui_province import GuiProvince, ProvinceType

import numpy
import json


class Map_LS:
    def __init__(self, map_size):
        self.map_size = map_size

        self.provinces_number_array = numpy.zeros(map_size, dtype=numpy.int8)
        self.provinces_number_array.fill(-1)

        self.tile_number_array = numpy.zeros(map_size, dtype=numpy.int8)
        self.tile_number_array.fill(-1)

    def load_map(self):
        with open("saved_maps/map1.json", "r") as json_file:
            provinces_json = json.load(json_file)

        provinces_neighboring = []

        for name in provinces_json["provinces"]:
            provinces_neighboring.append({"province": GuiProvince(name, provinces_json["provinces"][name]["province_type"], 
                                                      provinces_json["provinces"][name]["is_supply_center"], 
                                                      provinces_json["provinces"][name]["tiles"]),
                                          "neighboring": set()
                                         })
        
        for name in provinces_json["provinces"]:
            for nb in provinces_json["provinces"][name]["neighboring"]:
                for p_n in provinces_neighboring:
                    if int(p_n["province"].name) == nb:
                        provinces_neighboring[int(name)]["neighboring"].add(provinces_neighboring[nb]["province"])


        return provinces_neighboring                    

    def save_map(self):
        provinces_and_transitions_dict = {"provinces": dict()}

        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                province_number = int(self.provinces_number_array[x, y])

                if province_number in provinces_and_transitions_dict["provinces"]:
                    provinces_and_transitions_dict["provinces"][province_number]["tiles"].append((x, y))
                else:
                    provinces_and_transitions_dict["provinces"][province_number] = {
                        "tiles": [
                            (x, y)
                        ],
                        "is_supply_center": False, 
                        "province_type": None,
                        "neighboring": []
                    }

        for name in provinces_and_transitions_dict["provinces"]:
            x, y = provinces_and_transitions_dict["provinces"][name]["tiles"][0]
            if self.tile_number_array[x, y] == 0:
                provinces_and_transitions_dict["provinces"][name]["province_type"] = ProvinceType.land.value
            else:
                provinces_and_transitions_dict["provinces"][name]["province_type"] = ProvinceType.water.value
        

        for name in provinces_and_transitions_dict["provinces"]:
            for tile_coordinations in provinces_and_transitions_dict["provinces"][name]["tiles"]:
                x, y = tile_coordinations[0], tile_coordinations[1]
                
                if self.tile_number_array[x, y] == 1:
                    provinces_and_transitions_dict["provinces"][name]["is_supply_center"] = True
                
                for x_n in range(x-1, x+1):
                    if self.provinces_number_array[x_n, y] != self.provinces_number_array[x, y]:
                        if self.tile_number_array[x_n, y] == 2:
                            if self.tile_number_array[x, y] == 0:
                                if provinces_and_transitions_dict["provinces"][name]["province_type"] != ProvinceType.coast.value:
                                    provinces_and_transitions_dict["provinces"][name]["province_type"] = ProvinceType.coast.value
                        provinces_and_transitions_dict["provinces"][name]["neighboring"].append(int(self.provinces_number_array[x_n, y]))

                for y_n in range(y-1, y+1):
                    if self.provinces_number_array[x, y_n] != self.provinces_number_array[x, y]:
                        if self.tile_number_array[y, y_n] == 2:
                            if self.tile_number_array[x, y] == 0:
                                if provinces_and_transitions_dict["provinces"][name]["province_type"] != ProvinceType.coast.value:
                                    provinces_and_transitions_dict["provinces"][name]["province_type"] = ProvinceType.coast.value
                        provinces_and_transitions_dict["provinces"][name]["neighboring"].append(int(self.provinces_number_array[x, y_n]))



        with open("saved_maps/map1.json", "w") as json_file:
            json.dump(provinces_and_transitions_dict, json_file, indent=4)

    def add_province_tile(self, x, y, tile):
        self.tile_number_array[x, y] = tile

    def add_province_number(self, x, y, n):
        self.provinces_number_array[x, y] = n
