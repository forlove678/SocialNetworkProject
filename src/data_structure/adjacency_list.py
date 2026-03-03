class AdjacencyList:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph: self.graph[u] = []
        if v not in self.graph: self.graph[v] = []
        if v not in self.graph[u]: self.graph[u].append(v)
        if u not in self.graph[v]: self.graph[v].append(u)

    def get_neighbors(self, u):
        return self.graph.get(u, [])