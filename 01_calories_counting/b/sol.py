"""
Part 2: sum of top 3 elements
"""
import sys
from itertools import chain
import heapq


def main():
    n = 3
    heap = []
    current_sum = 0

    for line in chain(sys.stdin, [""]):
        if line.strip().isnumeric():
            amount = int(line)
            current_sum += amount
        elif current_sum > 0:
            heapq.heappush(heap, current_sum)
            current_sum = 0
            if len(heap) > n:
                heapq.heappop(heap)

    print(sum(heap))


if __name__ == "__main__":
    main()
