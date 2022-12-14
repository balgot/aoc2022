from typing import List, Tuple, Iterable
import math
from curses import wrapper, newpad
from curses.textpad import rectangle
import curses
import time


Coord = Tuple[int, int]
Block = List[Coord]
Blocks = List[Block]


OBSTACLE = "#"
AIR = " "
DROP = "o"


def _size(segs: Blocks) -> 'tuple[int, int]':
    mx, Mx = my, My = math.inf, -math.inf
    for s in segs:
        for y, x in s:
            mx = min(mx, x); Mx = max(Mx, x)
            my = min(my, y); My = max(My, y)
    return mx, Mx, my, My


def _diff(_from: int, _to: int) -> int:
    """Return unitary vector in the direction _from -> _to."""
    if _from == _to:
        return 0  # handle division by zero
    return (_to - _from) // abs(_to - _from)


class Game:
    """Represent the state of the falling sand.

    This class stores information about falling sand and obstacles and updates
    the corresponding window with the falling sand.

    Attributes
    ==========
        * width: width of the window used
        * height: height if the window
        * window: access to the drawn window (from `curses`)
        * steps: number of successfully stored sands (the score)

    Methods
    =======
        * step: coroutine, used to iteratively generate each step of the
            simulation, updates the drawing window

    """

    def __init__(self, obstacles: Blocks) -> None:
        # first get the width and height (source is added for convenience)
        SOURCE = [[(0, 500)]]
        small_x, big_x, small_y, big_y = _size(obstacles + SOURCE)

        # the final big_y
        big_y += 2
        self.height = big_y - small_y + 1

        # the min, max width is
        _msmall = 500 - self.height - 1
        _mbig = 500 + self.height + 1
        small_x, big_x = min(small_x, _msmall), max(big_x, _mbig)
        self.width = big_x - small_x + 1
        self._dx = small_x
        self._dy = small_y

        self._init_window()
        FLOOR = [(big_y, small_x), (big_y, big_x)]
        self._add_obstacles(obstacles + [FLOOR])

    def _init_window(self):
        """Initialize the window for drawing (fill with AIR)."""
        self.steps = 0
        self.window = newpad(self.height + 1, self.width)  # why +1? idk
        for y in range(self.height):
            for x in range(self.width):
                self.window.addch(y, x, AIR)

    def _add_obstacles(self, obstacles: Blocks):
        """Place the obstacles."""
        for block in obstacles:
            for i in range(len(block) - 1):
                (sy, sx), (ty, tx) = block[i], block[i+1]
                dx, dy = _diff(sx, tx), _diff(sy, ty)
                # draw line from (sx, sy) to (tx, ty)
                while (sy, sx) != (ty+dy, tx+dx):
                    self.window.addch(sy - self._dy, sx - self._dx, OBSTACLE)
                    sy, sx = sy+dy, sx+dx

    def _get(self, y, x) -> 'str | None':
        if 0 <= y < self.height and 0 <= x < self.width:
            return chr(self.window.inch(y, x) & 255)  # get only lower bits
        return None

    def _nxt(self, src: Coord) -> 'Coord | None':
        """Get next position for falling sand. None if outside the box."""
        y, x = src
        for next in [(y + 1, x), (y + 1, x - 1), (y + 1, x + 1)]:
            if self._get(*next) not in (OBSTACLE, DROP):
                return next
        return None

    def step(self, from_x: int = 500) -> 'Iterable[None]':
        while self._get(0, from_x - self._dx) == AIR:
            self.steps += 1
            prev = -1, from_x - self._dx
            dropping = self._nxt(prev)
            while dropping is not None:
                # first clear old sand
                if self._get(*prev):
                    self.window.addch(*prev, AIR)
                # then set new sand if we are inside the box
                if self._get(*dropping):
                    self.window.addch(*dropping, DROP)
                else:
                    return
                dropping, prev = self._nxt(dropping), dropping
                yield 3


def main(stdscr):
    """Perform the simulation.

    The game layout  looks as follows:
    vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    First line with data about score
    +-------------------------------+
    |
    |
    |
    | (The game to the full
    |       screen with and height)
    |
    |
    |
    |
    +--------------------------------+
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    TODO: Use WASD to move the current window.
    In the end, enters infinite cycle.
    """

    # read the data from the file
    segments: 'Blocks' = []
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            coords = line.split("->")
            _extract = lambda c: tuple(map(int, c.split(",")[::-1]))  # (y, x) order
            segments.append(list(map(_extract, coords)))

    # initialize the window
    curses.curs_set(0)  # invisible cursor
    curses.halfdelay(1)  # no-wait char reading
    maxy, maxx = stdscr.getmaxyx()  # max size

    # initialize the game with g-window
    game = Game(segments)
    bottom, right = min(game.height + 2, maxy) - 2, min(game.width + 1, maxx) - 2  # -2? idk but works
    rectangle(stdscr, 1, 0, bottom, right)
    stdscr.addstr(0, 0, f"Starting!")
    view = (0, 0)  # (y, x)

    # helpers
    def refresh():
        stdscr.refresh()
        game.window.refresh(*view, 2, 1, bottom - 1, right - 1)

    def handle_key():  # window.nodelay(flag) with True
        try:
            c = stdscr.getkey()
            _y, _x = view
            if c == "w": view = (_y - 1, _x)
            elif c == "a": view = (_y , _x - 1)
            elif c == "s": view = (_y + 1, _x)
            elif c == "d": view = (_y, _x + 1)
            else:
                raise RuntimeError(c)
            view = tuple(map(lambda x: max(x, 0), view))
        except:
            ...


    # the game simulation
    refresh()
    for i, _ in enumerate(game.step()):
        stdscr.addstr(0, 0, f"Score: {game.steps}")
        if i % 100 == 0: refresh()
        ## if i % 500 == 0: handle_key()
    refresh()
    while True:...



if __name__ == "__main__":
    wrapper(main)
