from typing import Generator
from graph_simulator.graph import Graph


def dfs(graph: Graph, start: int) -> Generator[tuple, None, None]:
    visited = set()

    def _helper(node: int) -> Generator[tuple, None, None]:
        visited.add(node)
        yield ("visit", node)

        for nei in graph.neighbors(node):
            if nei not in visited:
                yield ("discover", node, nei)
                yield from _helper(nei)

    yield from _helper(start)
