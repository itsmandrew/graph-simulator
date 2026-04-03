import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from graph_simulator.graph import Graph
from typing import Generator


class GraphVisualizer:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.G = nx.Graph()
        self.fig, self.ax = plt.subplots(figsize=(10, 7))

        for u, nei in graph.adjacency.items():
            for v, w in nei.items():
                self.G.add_edge(u, v, weight=w)

        self.pos = nx.spring_layout(self.G, seed=42)
        self.node_colors = {n: "#AED6F1" for n in self.G.nodes}
        self.edge_colors = {e: "#95A5A6" for e in self.G.edges}

    def _get_node_colors(self) -> list:
        return [self.node_colors[n] for n in self.G.nodes]

    def _get_edge_colors(self) -> list:
        return [self.edge_colors[e] for e in self.G.edges]

    def draw(self):
        self.ax.clear()
        nx.draw(
            self.G,
            self.pos,
            ax=self.ax,
            with_labels=True,
            node_color=self._get_node_colors(),
            edge_color=self._get_edge_colors(),
            node_size=700,
            font_size=12,
            font_color="white",
            font_weight="bold",
        )

    def animate(self, steps: Generator[tuple, None, None], interval: int = 600):
        steps_list: list[tuple] = list(steps)

        def update(i: int) -> list:
            step = steps_list[i]
            if step[0] == "visit":
                self.node_colors[step[1]] = "#E74C3C"
            elif step[0] == "discover":
                self.node_colors[step[2]] = "#F39C12"
                edge = (step[1], step[2])
                if edge in self.edge_colors:
                    self.edge_colors[edge] = "#E74C3C"
                elif (edge[1], edge[0]) in self.edge_colors:
                    self.edge_colors[(edge[1], edge[0])] = "#E74C3C"
            self.draw()
            return self.ax.get_children()

        ani = animation.FuncAnimation(
            self.fig,
            update,
            frames=len(steps_list),
            interval=interval,
            repeat=False,
        )
        plt.tight_layout()
        plt.show()
