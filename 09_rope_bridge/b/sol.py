import sys


_DIR = {
    "U": (1, 0),
    "D": (-1, 0),
    "L": (0, -1),
    "R": (0, 1)
}


def d(f, s):
    if f == s:
        return 0
    return (f - s) // abs(f - s)


def main():
    snake = [(0, 0) for _ in range(10)]
    visited = set()
    visited.add(snake[-1])

    for dir, steps in map(str.split, sys.stdin):
        steps = int(steps)
        dx, dy = _DIR[dir]
        for _ in range(steps):
            hx, hy = snake[0] = (snake[0][0] + dx, snake[0][1] + dy)
            for i in range(1, 10):
                tx, ty = snake[i]
                if max(abs(hx-tx), abs(hy-ty)) > 1:
                    snake[i] = (tx + d(hx, tx), ty + d(hy, ty))
                hx, hy = snake[i]
            visited.add(snake[-1])
    print(len(visited))




if __name__ == "__main__":
    main()
