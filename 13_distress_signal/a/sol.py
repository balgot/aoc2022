from itertools import zip_longest
from enum import Enum


class CMP(Enum):
    LEFT, EQ, RIGHT = -1, 0, 1


def _cmp(fst, snd) -> 'CMP':
    flist = isinstance(fst, list)
    slist = isinstance(snd, list)

    if not flist and not slist:
        if fst == snd: return CMP.EQ
        return CMP.LEFT if fst < snd else CMP.RIGHT

    fst = fst if flist else [fst]
    snd = snd if slist else [snd]

    for f, s in zip_longest(fst, snd, fillvalue=None):
        if f is None:
            return CMP.LEFT
        if s is None:
            return CMP.RIGHT
        if (c := _cmp(f, s)) != CMP.EQ:
            return c
    return CMP.EQ  # all equal


def main():
    lines = open(0).readlines()
    correct = 0
    for i in range(0, len(lines), 3):
        fst, snd = lines[i], lines[i+1]
        if _cmp(eval(fst), eval(snd)) != CMP.RIGHT:
            correct += i//3 + 1
    print(correct)


if __name__ == "__main__":
    main()
