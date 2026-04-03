from graph_simulator.graph import Graph
from graph_simulator.algorithms.bfs import bfs
from graph_simulator.algorithms.dfs import dfs
from graph_simulator.visualizer.canvas import GraphVisualizer


def main():
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for u, v in edges:
        g.add_edge(u, v)

    print("Select algorithm:")
    print("  1 = BFS")
    print("  2 = DFS")
    choice = input("> ").strip()

    if choice == "1":
        steps = bfs(g, start=0)
    elif choice == "2":
        steps = dfs(g, start=0)
    else:
        print("Invalid choice")
        return

    viz = GraphVisualizer(g)
    viz.animate(steps)


if __name__ == "__main__":
    main()
