import sys
from typing import Tuple, List
from tqdm import tqdm


_DBG = True
_dbg = lambda *args, **kwargs: print(*args, **kwargs) if _DBG else ()


Coord = Tuple[int, int]  # (x, y)


def _dist(pos1: Coord, pos2: Coord) -> int:
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def parse_input() -> Tuple[List[Coord], List[Coord]]:
    sensors = []
    beacons = []
    extr = lambda s: int(s.rstrip(",").rstrip(":").rsplit("=", maxsplit=1)[1])

    for line in sys.stdin:
        _sensor, _at, x, y, _closest, _beacon, _is, _at, xx, yy = line.split()
        x, y, xx, yy = map(extr, (x, y, xx, yy))
        sensors.append((x, y))
        beacons.append((xx, yy))

    return sensors, beacons


def _dir(a: Coord, b: Coord):
    ax, ay = a
    bx, by = b
    _dd = lambda f, t: 0 if f == t else (t - f) // abs(t - f)
    return _dd(ax, bx), _dd(ay, by)


def main(low, upper, mul):
    # observation: the only position must be just on the edge
    #   of forbidden positions for at least one sensor
    sensors, beacons = parse_input()
    possible = set()
    inside = lambda x, y: low <= x <= upper and low <= y <= upper
    for s, b in zip(tqdm(sensors), beacons):
        x, y = s
        dist = _dist(s, b)

        LEFT =  (x - dist - 1, y)
        RIGHT = (x + dist + 1, y)
        UP =    (x, y - dist - 1)
        DOWN =  (x, y + dist + 1)

        DIRS = [LEFT, UP, RIGHT, DOWN, LEFT]

        for start, end in zip(DIRS, DIRS[1:]):
            dx, dy = _dir(start, end)
            sx, sy = start
            ex, ey = end
            while (sx, sy) != (ex + dx, ey + dy):
                if inside(sx, sy):
                    possible.add((sx, sy))
                sx, sy = sx+dx, sy+dy

    possible -= set( beacons )
    _result = set()
    for p in tqdm(possible):
        ok = True
        for ss, bb in zip(sensors, beacons):
            if _dist(ss, p) <= _dist(ss, bb):
                ok = False
                break
        if ok:
            _result.add(p)

    _dbg(_result)
    assert len(_result) == 1
    x, y = _result.pop()
    print(x*mul + y)


if __name__ == "__main__":
    # main(low=0, upper=20, mul=4000000)
    main(low=0, upper=4000000, mul=4000000)
