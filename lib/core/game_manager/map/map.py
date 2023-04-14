from .province import Province
from .unit import Unit

class Map:
    """Playing field. Stores all units and provinces"""

    def __init__(self):
        self.provinces_graph = dict()
        self.units = set()
    
    def add_province(self, new_province: Province, neighboring_provinces: [Province]):
        """Add a new province to the map

        Args:
            new_province (Province): Province to be added
            neighboring_provinces (Province]): List of neighboring provinces. May be empty. If it includes provinces that have not yet been added, they will be automatically added
        """
        if new_province not in self.provinces_graph:
            self.provinces_graph[new_province] = set(neighboring_provinces)
        else:
            for pr in neighboring_provinces:
                self.provinces_graph[new_province].add(pr)

        for province in neighboring_provinces:
            if province in self.provinces_graph:
                self.provinces_graph[province].add(new_province)
            else:
                self.provinces_graph[province] = set([new_province])

    def add_transition(self, first_province: Province, second_province: Province):
        """Adds a transition between two provinces.

        Args:
            first_province (Province): 
            second_province (Province): 
        """
        self.provinces_graph[first_province].add(second_province)

    def add_unit(self, unit):
        """Add a unit to the selected province

        Args:
            location (Province): The province in which there will be an amiya
        """
        self.units.add(unit)
        
        # In the future, if the provinces have their own protection, it may be necessary. In the meantime...
        #unit.location.protection = unit.protection

