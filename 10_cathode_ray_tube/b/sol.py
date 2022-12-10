import math
import sys
from textwrap import wrap


WIDTH = 40
HEIGHT = 6
LIT = "#"
DARK = "."


def main():
    X = 2
    res = []
    i = 1

    for line in sys.stdin:
        line = line.strip()
        cmd, *b = line.split()

        inside = X-1 <= i % WIDTH <= X+1
        res.append(LIT if inside else DARK)
        i += 1

        if cmd == "addx":
            inside = X-1 <= i % WIDTH <= X+1
            res.append(LIT if inside else DARK)
            X += int(b[0])
            i += 1

    print("\n".join(wrap("".join(res), width=WIDTH)))


if __name__ == "__main__":
    main()
