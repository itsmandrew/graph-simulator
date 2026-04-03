from graph_simulator.graph import Graph
from graph_simulator.algorithms.bfs import bfs
from graph_simulator.algorithms.dfs import dfs
from graph_simulator.algorithms.bfs_matrix import bfs_matrix
from graph_simulator.algorithms.dfs_matrix import dfs_matrix
from graph_simulator.visualizer.canvas import GraphVisualizer, GridVisualizer

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RED = "\033[91m"
DIM = "\033[2m"


def _banner():
    print(f"\n{BOLD}{CYAN}  ┌─────────────────────────┐")
    print(f"  │    graph  simulator     │")
    print(f"  └─────────────────────────┘{RESET}\n")


def _pick(label: str, options: list[tuple[str, str]]) -> str:
    """Render a labeled menu and return the chosen value."""
    keys = {str(i + 1): val for i, (_, val) in enumerate(options)}
    keys |= {val: val for _, val in options}

    print(f"  {BOLD}{label}{RESET}")
    for i, (display, val) in enumerate(options, 1):
        print(f"  {BLUE}{BOLD} {i}{RESET}{DIM} ·{RESET}  {display}")

    shorthand = " / ".join(f"{i+1}" for i in range(len(options)))
    while True:
        try:
            raw = input(f"\n  {DIM}[{shorthand}]{RESET}  ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit(0)
        if raw in keys:
            chosen = keys[raw]
            name = next(d for d, v in options if v == chosen)
            print(f"  {DIM}→ {name}{RESET}\n")
            return chosen
        print(f"  {RED}'{raw}' is not a valid choice{RESET}")


SAMPLE_MATRIX = [
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1],
]
MATRIX_START = (0, 0)


def main():
    _banner()
    graph_type = _pick("Graph type", [("Adjacency list", "adjlist"), ("2D matrix / grid", "grid")])

    if graph_type == "grid":
        algo = _pick("Algorithm", [("Breadth-first search  (BFS)", "bfs"), ("Depth-first search   (DFS)", "dfs")])
        steps = bfs_matrix(SAMPLE_MATRIX, MATRIX_START) if algo == "bfs" else dfs_matrix(SAMPLE_MATRIX, MATRIX_START)
        viz = GridVisualizer(SAMPLE_MATRIX, algo=algo)
        viz.animate(steps)
    else:
        g = Graph()
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        for u, v in edges:
            g.add_edge(u, v)

        mode = _pick("Display mode", [("Tree", "tree"), ("Adjacency matrix", "matrix")])
        algo = _pick("Algorithm", [("Breadth-first search  (BFS)", "bfs"), ("Depth-first search   (DFS)", "dfs")])

        steps = bfs(g, start=0) if algo == "bfs" else dfs(g, start=0)
        viz = GraphVisualizer(g, mode=mode, algo=algo)
        viz.animate(steps, root=0)


if __name__ == "__main__":
    main()
