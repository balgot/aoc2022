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
    lines = map(eval, filter(None, map(str.strip, lines)))
    lines = list(lines)

    res = 1
    for i, L in enumerate(([[2]], [[6]])):
        smaller = sum(_cmp(x, L) == CMP.LEFT for x in lines)
        res *= (i + smaller + 1)  # i=<[2] is less than [6], +1=reindexing from 1
    print(res)


if __name__ == "__main__":
    main()
