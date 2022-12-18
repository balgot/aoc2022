import sys
from typing import Tuple, List


_DBG = False
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


def main(line: int):
    sensors, beacons = parse_input()
    cannot_be = set()
    for s, b in zip(sensors, beacons):
        x, y = s
        dist = _dist(s, b) - abs(line - y)
        _dbg(f"s={s}, b={b}, dist={dist}")
        for pos in range(-dist, dist + 1):
            cannot_be.add(pos + x)
    for x, y in beacons:
        if y == line:
            cannot_be.discard(x)
    print(len(cannot_be))


if __name__ == "__main__":
    main(line=2000000)
