import sys


def vis(map: 'list[list[int]]', visible: 'list[list[bool]]', x, y, dx, dy):
    max_height = -float("inf")
    while 0 <= x < len(map) and 0 <= y < len(map[0]):
        if map[x][y] > max_height:
            visible[x][y] = True
        max_height = max(max_height, map[x][y])
        x += dx
        y += dy


def main():
    grid = [[int(h) for h in line.strip()] for line in sys.stdin]
    visi = [[False for _ in r] for r in grid]
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        _iter = range(len(grid)) if dx else range(len(grid[0]))
        for i in _iter:
            if dx:
                y = i
                x = 0 if dx > 0 else len(grid[0]) - 1
            else:
                y = 0 if dy > 0 else len(grid) - 1
                x = i
            vis(grid, visi, x, y, dx, dy)
    print(sum(sum(row) for row in visi))



if __name__ == "__main__":
    main()
