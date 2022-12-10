import math
import sys


def main():
    X = 1
    i = 1
    s = 0

    CYCLES = {20, 60, 100, 140, 180, 220}

    for line in sys.stdin:
        line = line.strip()
        cmd, *b = line.split()
        if i in CYCLES:
            s += X * i
        i += 1
        if cmd == "addx":
            if i in CYCLES:
                s += X * i
            X += int(b[0])
            i += 1

    print(s)


if __name__ == "__main__":
    main()
