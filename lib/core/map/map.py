from .province import Province

class Map:
    def __init__(self):
        self.provinces_graph = dict()
    
    def add_province(self, new_province: Province, neighboring_provinces: [Province]):
        self.provinces_graph[new_province] = set(neighboring_provinces)

        for pr in neighboring_provinces:
            if pr in self.provinces_graph:
                self.provinces_graph[pr].add(new_province)
            else:
                self.provinces_graph[pr] = set([new_province])

    def add_connection(self, first_province: Province, second_province: Province):
        self.provinces_graph[first_province].add(second_province)
