"""
Calories counting
=================

(read input from stdin)
"""
import sys
import math


def main():
    best = -math.inf
    current = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            best = max(best, current)
            current = 0
        else:
            current += int(line)
    print(max(best, current))


if __name__ == "__main__":
    main()
