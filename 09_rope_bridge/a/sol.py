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
    head = tail = (0, 0)
    visited = set()
    visited.add(tail)

    for dir, steps in map(str.split, sys.stdin):
        steps = int(steps)
        dx, dy = _DIR[dir]
        for _ in range(steps):
            tx, ty = tail
            hx, hy = head = (head[0] + dx, head[1] + dy)
            if max(abs(hx-tx), abs(hy-ty)) > 1:
                tail = (tx + d(hx, tx), ty + d(hy, ty))
            visited.add(tail)
    print(len(visited))




if __name__ == "__main__":
    main()
