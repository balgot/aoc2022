import sys
from collections import deque
from dataclasses import dataclass, astuple


_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def can_move(self, x, y, tx, ty):
        return (self.inside(x, y)
            and self.inside(tx, ty)
            and self.grid[y][x] + 1 >= self.grid[ty][tx]
        )

    def bfs(self, sy, sx, ty, tx):
        @dataclass
        class _Loc:
            x: int
            y: int
            steps: int

        q = deque([_Loc(sx, sy, 0)])
        visited = set((sx, sy))
        while q:
            x, y, steps = astuple(q.popleft())
            # print(f"[{x}, {y}] in {steps}")
            if (x, y) == (tx, ty):
                return steps
            for dx, dy in _DIRS:
                nx, ny = x+dx, y+dy
                if self.can_move(x, y, nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append(_Loc(nx, ny, steps+1))
        return None


def main():
    lines = list(map(str.strip, sys.stdin))
    m = Map(len(lines[0]), len(lines))
    start = None
    target = None
    for i, row in enumerate(lines):
        for j, e in enumerate(row):
            if e == "S":
                m.grid[i][j] = 0
                start = (i, j)
            elif e == "E":
                m.grid[i][j] = ord("z") - ord("a")
                target = (i, j)
            else:
                m.grid[i][j] = ord(e) - ord("a")
    assert start and target
    steps = m.bfs(*start, *target)
    assert steps is not None
    print(steps)


if __name__ == "__main__":
    main()
