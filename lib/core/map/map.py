from .province import Province

class Map:
    def __init__(self):
        self.provinces_graph = dict()
    
    def add_province(self, new_province: Province, neighboring_provinces: [Province]):
        self.provinces_graph[new_province] = set(neighboring_provinces)

        for pr in neighboring_provinces:
            self.provinces_graph[pr].add(new_province)
