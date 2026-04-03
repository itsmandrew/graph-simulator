from typing import Generator


def dfs_matrix(matrix: list[list[int]], start: tuple[int, int]) -> Generator[tuple, None, None]:
    rows, cols = len(matrix), len(matrix[0])
    visited = set()

    def _helper(r: int, c: int) -> Generator[tuple, None, None]:
        visited.add((r, c))
        yield ("visit", (r, c))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] == 1 and (nr, nc) not in visited:
                yield ("discover", (r, c), (nr, nc))
                yield from _helper(nr, nc)

    yield from _helper(*start)
