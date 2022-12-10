import sys

DBG = False
_dbg = lambda *args, **kwargs: print(*args, **kwargs) if DBG else ()


def score(grid: 'list[list[int]]', x, y) -> int:
    _DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    s = 1
    _dbg(f"(y, x) = (row, col) = ({y}, {x})\tvalue = {grid[y][x]}")
    for dx, dy in _DIRS:
        nx, ny = x + dx, y + dy
        curr = 0
        while 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            curr += 1
            if grid[ny][nx] >= grid[y][x]:
                break
            nx, ny = nx + dx, ny + dy
        _dbg(f"\t<{dy}, {dx}>  -->", curr)
        s *= curr
    _dbg(f"== score: {s}")
    return s


def main():
    grid = [[int(h) for h in line.strip()] for line in sys.stdin]
    best = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            best = max(best, score(grid, x, y))
    print(best)


if __name__ == "__main__":
    main()
