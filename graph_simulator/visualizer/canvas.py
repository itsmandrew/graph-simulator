import os
from typing import Generator
from graph_simulator.graph import Graph


# ANSI color codes
RESET = "\033[0m"
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BOLD = "\033[1m"
DIM = "\033[2m"


class GraphVisualizer:
    def __init__(self, graph: Graph, mode: str = "tree", algo: str = "bfs"):
        self.graph = graph
        self.mode = mode  # "tree" or "matrix"
        self.algo = algo
        self.node_states: dict[int, str] = {n: "unvisited" for n in graph.nodes}

    # ─────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _color_node(self, node: int) -> str:
        state = self.node_states[node]
        label = f"[{node}]"
        if state == "visiting":
            return f"{RED}{BOLD}{label}{RESET}"
        elif state == "discovered":
            return f"{YELLOW}{label}{RESET}"
        elif state == "visited":
            return f"{GREEN}{label}{RESET}"
        else:
            return f"{BLUE}{label}{RESET}"

    def _header(self, step_num: int | None = None, total: int | None = None):
        mode_label = "Tree" if self.mode == "tree" else "Matrix"
        algo_label = self.algo.upper()
        if step_num is not None:
            progress = f"  step {step_num}/{total}"
        else:
            progress = "  ready"
        line = f"  {BOLD}{algo_label}{RESET}  {mode_label}   {DIM}{progress}{RESET}"
        print(line)
        print(f"  {DIM}{'─' * 36}{RESET}")

    def _legend(self):
        parts = [
            f"{BLUE}[n]{RESET} unvisited",
            f"{RED}{BOLD}[n]{RESET} visiting",
            f"{YELLOW}[n]{RESET} discovered",
            f"{GREEN}[n]{RESET} visited",
        ]
        print(f"  {DIM}" + "   ".join(parts) + f"{RESET}")

    def _wait(self, step_num: int, total: int, message: str):
        print(f"\n  {DIM}↳{RESET} {message}")
        try:
            input(f"  {DIM}[enter]{RESET} ")
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit(0)

    # ─────────────────────────────────────────
    # TREE MODE
    # ─────────────────────────────────────────

    def _build_tree_lines(self, root: int) -> list[str]:
        lines = []

        def _render(node: int, parent: int | None, prefix: str, is_left: bool, is_root: bool):
            if is_root:
                lines.append(f"  {self._color_node(node)}")
            else:
                connector = "├────── " if is_left else "└────── "
                lines.append(f"  {prefix}{connector}{self._color_node(node)}")

            children = [n for n in self.graph.neighbors(node) if n != parent]
            for i, neighbor in enumerate(children):
                is_last = i == len(children) - 1
                if is_root:
                    new_prefix = ""
                else:
                    new_prefix = prefix + ("│      " if is_left else "       ")
                _render(neighbor, node, new_prefix, not is_last, False)

        _render(root, None, "", True, True)
        return lines

    def _draw_tree(self, root: int):
        lines = self._build_tree_lines(root)
        print()
        for line in lines:
            print(line)
        print()

    # ─────────────────────────────────────────
    # MATRIX MODE
    # ─────────────────────────────────────────

    def _draw_matrix(self):
        nodes = sorted(self.graph.nodes)
        col_width = 8

        # Header row
        header = "     " + "".join(str(n).center(col_width) for n in nodes)
        print()
        print(f"  {BOLD}{header}{RESET}")

        for u in nodes:
            row = f"  {self._color_node(u)} "
            for v in nodes:
                if v in self.graph.neighbors(u):
                    weight = self.graph.neighbors(u)[v]
                    cell = f"{weight:.0f}".center(col_width)
                    # Color the cell based on state of v
                    state = self.node_states[v]
                    if state == "visiting":
                        row += f"{RED}{BOLD}{cell}{RESET}"
                    elif state == "discovered":
                        row += f"{YELLOW}{cell}{RESET}"
                    elif state == "visited":
                        row += f"{GREEN}{cell}{RESET}"
                    else:
                        row += cell
                else:
                    row += "   .   "
            print(row)
        print()

    # ─────────────────────────────────────────
    # DRAW DISPATCHER
    # ─────────────────────────────────────────

    def draw(self, root: int = 0, step_num: int | None = None, total: int | None = None):
        self._clear()
        print()
        self._header(step_num, total)
        print()
        if self.mode == "tree":
            self._draw_tree(root)
        elif self.mode == "matrix":
            self._draw_matrix()
        self._legend()

    # ─────────────────────────────────────────
    # ANIMATE
    # ─────────────────────────────────────────

    def animate(self, steps: Generator[tuple, None, None], root: int = 0):
        steps_list: list[tuple] = list(steps)
        total = len(steps_list)

        self.draw(root, step_num=0, total=total)
        try:
            input(f"\n  {DIM}[enter] to start{RESET}  ")
        except (EOFError, KeyboardInterrupt):
            print()
            return

        for i, step in enumerate(steps_list):
            if step[0] == "visit":
                self.node_states[step[1]] = "visiting"
                message = f"visiting node {BOLD}{step[1]}{RESET}"
            elif step[0] == "discover":
                self.node_states[step[1]] = "visited"
                self.node_states[step[2]] = "discovered"
                message = f"discovered {BOLD}{step[2]}{RESET} from {BOLD}{step[1]}{RESET}"
            else:
                message = str(step)

            self.draw(root, step_num=i + 1, total=total)
            self._wait(i + 1, total, message)

        # Mark all remaining discovered as visited
        for node in self.node_states:
            if self.node_states[node] in ("visiting", "discovered"):
                self.node_states[node] = "visited"

        self.draw(root, step_num=total, total=total)
        print(f"\n  {GREEN}{BOLD}done{RESET}  {DIM}all {total} steps complete{RESET}\n")


class GridVisualizer:
    WALL = "██"
    OPEN = "  "

    def __init__(self, matrix: list[list[int]], algo: str = "bfs"):
        self.matrix = matrix
        self.algo = algo
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.cell_states: dict[tuple[int, int], str] = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if matrix[r][c] == 1:
                    self.cell_states[(r, c)] = "unvisited"

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _color_cell(self, r: int, c: int) -> str:
        if self.matrix[r][c] == 0:
            return f"{DIM}████{RESET}"
        state = self.cell_states.get((r, c), "unvisited")
        if state == "visiting":
            return f"{RED}{BOLD}●●●●{RESET}"
        elif state == "discovered":
            return f"{YELLOW}◉◉◉◉{RESET}"
        elif state == "visited":
            return f"{GREEN}◉◉◉◉{RESET}"
        else:
            return f"{BLUE}····{RESET}"

    def _header(self, step_num: int | None = None, total: int | None = None):
        algo_label = self.algo.upper()
        progress = f"step {step_num}/{total}" if step_num is not None else "ready"
        print(f"  {BOLD}{algo_label}{RESET}  Grid   {DIM}{progress}{RESET}")
        print(f"  {DIM}{'─' * 36}{RESET}")

    def _legend(self):
        parts = [
            f"{BLUE}····{RESET} unvisited",
            f"{RED}{BOLD}●●●●{RESET} visiting",
            f"{YELLOW}◉◉◉◉{RESET} discovered",
            f"{GREEN}◉◉◉◉{RESET} visited",
            f"{DIM}████{RESET} wall",
        ]
        print(f"  {DIM}" + "   ".join(parts) + f"{RESET}")

    def _draw_grid(self):
        border = "  +" + "----+" * self.cols
        print()
        print(border)
        for r in range(self.rows):
            row = "  |"
            for c in range(self.cols):
                row += self._color_cell(r, c) + "|"
            print(row)
            print(border)
        print()

    def draw(self, step_num: int | None = None, total: int | None = None):
        self._clear()
        print()
        self._header(step_num, total)
        self._draw_grid()
        self._legend()

    def animate(self, steps: Generator[tuple, None, None]):
        steps_list = list(steps)
        total = len(steps_list)

        self.draw(step_num=0, total=total)
        try:
            input(f"\n  {DIM}[enter] to start{RESET}  ")
        except (EOFError, KeyboardInterrupt):
            print()
            return

        for i, step in enumerate(steps_list):
            if step[0] == "visit":
                self.cell_states[step[1]] = "visiting"
                r, c = step[1]
                message = f"visiting cell {BOLD}({r},{c}){RESET}"
            elif step[0] == "discover":
                self.cell_states[step[1]] = "visited"
                self.cell_states[step[2]] = "discovered"
                r1, c1 = step[1]
                r2, c2 = step[2]
                message = f"discovered {BOLD}({r2},{c2}){RESET} from {BOLD}({r1},{c1}){RESET}"
            else:
                message = str(step)

            self.draw(step_num=i + 1, total=total)
            print(f"\n  {DIM}↳{RESET} {message}")
            try:
                input(f"  {DIM}[enter]{RESET} ")
            except (EOFError, KeyboardInterrupt):
                print()
                return

        for cell in self.cell_states:
            if self.cell_states[cell] in ("visiting", "discovered"):
                self.cell_states[cell] = "visited"

        self.draw(step_num=total, total=total)
        print(f"\n  {GREEN}{BOLD}done{RESET}  {DIM}all {total} steps complete{RESET}\n")
