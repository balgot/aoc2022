import sys
from typing import Tuple, List, Set
from tqdm import trange

# 0 is at ground level


Coord = Tuple[int, int]  # (y, x)
Block = List[Coord]

BLOCKS = [
    [(0,0), (0,1), (0,2), (0,3)],  # -
    [(0,1), (1,0), (1,1), (1,2), (2,1)],  # +
    [(0,2), (0,1), (0,0), (1,2), (2,2)],  # L
    [(0,0), (1,0), (2,0), (3,0)],  # I
    [(0,0), (0,1), (1,0), (1,1)]  # #
]
LEFT, RIGHT = "<", ">"
DIRS = input().strip()


class Arena:
    def __init__(self, width) -> None:
        self.width = width
        self.fixed: Set[Coord] = set()
        self.height: int = 0

    def spawn(self, n) -> Block:
        b = BLOCKS[n % len(BLOCKS)].copy()
        # first the left edge
        left = min(x for _, x in b)
        x_shift = max(0, 2 - left)
        # now bottom
        bottom = min(y for y, _ in b)
        y_shift = max(0, 3+self.height-bottom)
        # final block is..
        return self.move(b, x_shift, y_shift)

    def _outside(self, y, x) -> bool:
        return y < 0 or x < 0 or x >= self.width

    def can_move(self, b: Block, dx, dy) -> bool:
        for y, x in b:
            if (y+dy, x+dx) in self.fixed or self._outside(y+dy, x+dx):
                return False
        return True

    def move(self, b: Block, dx, dy) -> Block:
        return [(y+dy, x+dx) for y, x in b]

    def simulate(self, steps: int) -> None:
        _block = _dir = 0
        for s in range(steps):  # trange
            b = self.spawn(_block)
            _block += 1
            while True:
                # horizontal shift
                shift = DIRS[_dir % len(DIRS)]
                _dir += 1
                dx = -1 if shift == LEFT else 1
                if self.can_move(b, dx, 0):
                    b = self.move(b, dx, 0)
                # vertical shift
                if self.can_move(b, 0, -1):
                    b = self.move(b, 0, -1)
                else:
                    for pos in b:
                        assert pos not in self.fixed
                        self.fixed.add(pos)
                        self.height = max(self.height, pos[0] + 1)
                    break
            # print("\n\nAfter step", s+1)
            # dbg_arena(self)

def dbg_arena(a: Arena):
    lines = [["."]*a.width for _ in range(a.height+1)]
    for y, x in a.fixed:
        lines[y][x] = "#"
    for row in reversed(lines):
        print("|" + "".join(row) + "|")
    print("+" + "-"*a.width + "+")


def main(steps):
    arena = Arena(width=7)
    arena.simulate(steps)
    print(arena.height)
    # dbg_arena(arena)


if __name__ == "__main__":
    main(steps=2022)
