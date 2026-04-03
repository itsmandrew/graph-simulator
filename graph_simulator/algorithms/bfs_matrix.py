from collections import deque
from typing import Generator


def bfs_matrix(matrix: list[list[int]], start: tuple[int, int]) -> Generator[tuple, None, None]:
    rows, cols = len(matrix), len(matrix[0])
    visited = set([start])
    queue = deque([start])

    while queue:
        r, c = queue.popleft()
        yield ("visit", (r, c))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] == 1 and (nr, nc) not in visited:
                visited.add((nr, nc))
                yield ("discover", (r, c), (nr, nc))
                queue.append((nr, nc))
