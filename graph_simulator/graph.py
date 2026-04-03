from dataclasses import dataclass, field


@dataclass
class Graph:
    directed: bool = False
    adjacency: dict = field(default_factory=dict)

    def add_node(self, node: int):
        if node not in self.adjacency:
            self.adjacency[node] = {}

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        self.add_node(u)
        self.add_node(v)
        self.adjacency[u][v] = weight
        if not self.directed:
            self.adjacency[v][u] = weight

    def neighbors(self, node: int):
        return self.adjacency.get(node, {})

    @property
    def nodes(self):
        return list(self.adjacency.keys())
