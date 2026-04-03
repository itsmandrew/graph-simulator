# graph-simulator

An interactive terminal tool for visualizing graph traversal algorithms step-by-step.

## Features

- **BFS and DFS** on both adjacency list graphs and 2D grids
- **Step-by-step animation** — walk through each algorithm decision interactively
- **Multiple display modes** — tree view, adjacency matrix, or grid layout
- **Color-coded node states:**
  - Blue — unvisited
  - Red — currently visiting
  - Yellow — discovered (queued)
  - Green — fully visited

## Algorithms

| Algorithm | Adjacency List | 2D Grid |
|-----------|---------------|---------|
| BFS       | ✓             | ✓       |
| DFS       | ✓             | ✓       |
| Dijkstra  | planned       | —       |

## Setup

Requires Python 3.11+ and [Poetry](https://python-poetry.org/).

```bash
poetry install
```

## Usage

```bash
poetry run graph-sim
```

An interactive menu will guide you through selecting an algorithm and data structure. Press Enter to step through the visualization one frame at a time.

## Project Structure

```
graph_simulator/
├── main.py              # CLI entry point and menu
├── graph.py             # Adjacency list graph structure
├── algorithms/
│   ├── bfs.py           # BFS on adjacency list
│   ├── dfs.py           # DFS on adjacency list
│   ├── bfs_matrix.py    # BFS on 2D grid
│   └── dfs_matrix.py    # DFS on 2D grid
└── visualizer/
    └── canvas.py        # Terminal rendering engine
```
