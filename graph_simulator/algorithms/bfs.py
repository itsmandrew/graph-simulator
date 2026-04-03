from collections import deque
from typing import Generator
from graph_simulator.graph import Graph


def bfs(graph: Graph, start: int) -> Generator[tuple, None, None]:
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        yield ("visit", node)

        for nei in graph.neighbors(node):
            if nei not in visited:
                visited.add(nei)
                yield ("discover", node, nei)
                queue.append(nei)
