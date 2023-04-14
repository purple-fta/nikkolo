from .province import Province
from .unit import Unit

class Map:
    def __init__(self):
        self.provinces_graph = dict()
        self.units = set()
    
    def add_province(self, new_province: Province, neighboring_provinces: [Province]):
        self.provinces_graph[new_province] = set(neighboring_provinces)

        for pr in neighboring_provinces:
            if pr in self.provinces_graph:
                self.provinces_graph[pr].add(new_province)
            else:
                self.provinces_graph[pr] = set([new_province])

    def add_connection(self, first_province: Province, second_province: Province):
        self.provinces_graph[first_province].add(second_province)

<<<<<<< Updated upstream
    def add_unit(self, location: Province):
        self.units.add(Unit(location))
=======
    def add_unit(self, unit):
        """Add a unit to the selected province

        Args:
            location (Province): The province in which there will be an amiya
        """
        self.units.add(unit)
        
        # In the future, if the provinces have their own protection, it may be necessary. In the meantime...
        #unit.location.protection = unit.protection
>>>>>>> Stashed changes
