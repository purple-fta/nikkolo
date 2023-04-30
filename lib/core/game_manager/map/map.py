from .province import Province, ProvinceType
from .country import Country
from .unit import Unit

class Map:
    """Playing field. Stores all units and provinces"""

    def __init__(self):
        self.provinces_graph = dict()
        self.units = set()
        self.countries = []
    

    def add_province(self, new_province: Province, neighboring_provinces: [Province]):
        """Add a new province to the map

        Args:
            new_province (Province): Province to be added
            neighboring_provinces (Province]): List of neighboring provinces. May be empty. If it includes provinces that have not yet been added, they will be automatically added
        """
        
        # Type checking
        if not issubclass(type(new_province), Province):
            raise TypeError("The first argument has the wrong type")
        if type(neighboring_provinces) != list:
            raise TypeError("The second argument has the wrong type")
        
        # Need to check the type in the list
        else: 
            for i in neighboring_provinces:
                if not issubclass(type(i), Province):
                    raise TypeError("The second argument has the wrong type")

        # If a new province has already been added before, then we add neighbors to it
        if new_province not in self.provinces_graph:
            self.provinces_graph[new_province] = set(neighboring_provinces)
        
        # If the neighboring provinces have not yet been created, then you need to create
        for pr in neighboring_provinces:
            if pr not in self.provinces_graph:
                self.provinces_graph[pr] = set()

        # In neighboring provinces, you need to add a new province as a neighbor
        for province in neighboring_provinces:
            self.add_transition(new_province, province)

    def add_transition(self, first_province: Province, second_province: Province):
        """Adds a transition between two provinces.

        Args:
            first_province (Province): 
            second_province (Province): 
        """
        
        # Type checking
        if not issubclass(type(first_province), Province):
            raise TypeError("The first argument has the wrong type")
        if not issubclass(type(second_province), Province):
            raise TypeError("The second argument has the wrong type")
        
        # If incompatible types of provinces are adjacent
        if first_province.province_type == ProvinceType.land.value: 
            if second_province.province_type == ProvinceType.water.value:
                raise ValueError("Inappropriate types for neighboring provinces")
        if first_province.province_type == ProvinceType.water.value: 
            if second_province.province_type == ProvinceType.land.value:
                raise ValueError("Inappropriate types for neighboring provinces")

        # Adding a transition for both provinces
        self.provinces_graph[first_province].add(second_province)
        self.provinces_graph[second_province].add(first_province)

    def add_unit(self, new_unit: Unit, country: Country = None):
        """Add a unit to the selected province

        Args:
            location (Province): The province in which there will be an amiya
        """
        
        # Type checking
        if not issubclass(type(new_unit), Unit):
            raise TypeError("The first argument has the wrong type")

        # Value checking
        if not new_unit.location.is_supply_center:
            raise TypeError("Unit spawning is allowed in the CA only")

        # If the unit could already be created in that province
        for unit in self.units:
            if unit.location == new_unit.location:
                return

        if country:
            country.units.add(new_unit)

        self.units.add(new_unit)

    def add_country(self, country: Country):
        # Type Checking
        if not issubclass(type(country), Country):
            raise TypeError("The first argument has the wrong type")

        self.countries.append(country)

    def add_province_to_country(self, province, country):
        for c in self.countries:
            if province in c.provinces:
                c.provinces.remove(province)
        country.provinces.add(province)
