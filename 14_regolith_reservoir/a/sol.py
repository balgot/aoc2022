import sys
from typing import List, Tuple
import math
from curses import wrapper, newpad
from curses.textpad import rectangle


Coord = Tuple[int, int]
Block = List[Coord]
Blocks = List[Block]


OBSTACLE = "#"
AIR = "."


def _size(segs: Blocks) -> 'tuple[int, int]':
    mx, Mx = my, My = math.inf, -math.inf
    for s in segs:
        for x, y in s:
            mx = min(mx, x); Mx = max(Mx, x)
            my = min(my, y); My = max(My, y)

    width = Mx - mx
    height = My- my
    return width, height


def draw_obstacles(wdw, segs: Blocks, w: int, h: int):
    # raise RuntimeError(wdw.getmaxyx())
    for i in range(w):
        for j in range(h):
            try:
                wdw.addch(j, i, AIR)
            except Exception as e:
                cause = f"""
                    Was {wdw.getmaxyx()},
                    but setting ({1+j-h}, {1+i-w})
                """
                raise RuntimeError(cause) from e


    for s in segs:
        for i in range(1, len(s)):
            fx, fy = s[i-1]
            sx, sy = s[i]
            _d = lambda f, s: 0 if f == s else (s - f) // abs(s - f)
            dx, dy = _d(fx, fy), _d(sx, sy)
            while (fx, fy) != (sx + dx, sy + dy):
                # wdw.addch(fy - h, fx - w, OBSTACLE)
                try:
                    wdw.addch(fy - h, fx - w, OBSTACLE)
                except Exception as e:
                    ## TODO: need mx, my
                    cause = f"""
                        Segment:
                            {(fy, fx)} -> {(sy, sx)}

                        Was {wdw.getmaxyx()},
                        but setting ({fy-h}, {fx-w})
                    """
                    raise RuntimeError(cause) from e

                fx, fy = fx + dx, fy + dy



def main(stdscr):
    segments: 'Blocks' = []
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            coords = line.split("->")
            _extract = lambda c: tuple(map(int, c.split(",")))
            segments.append(list(map(_extract, coords)))

    w, h = _size(segments)
    pad = newpad(1 + h + 1, 1 + w + 1)
    #print(w, h)
    rectangle(pad, 1, 0, 20, 20)  # height, width
    #stdscr.addch(5, 6, "A")
    #stdscr.addch(2, 3, "B")
    draw_obstacles(pad, segments, w, h)
    # pad.refresh(0, 0, 0, 0, 20, 20)
    while True:...
    print(type(stdscr))


if __name__ == "__main__":
    wrapper(main)
