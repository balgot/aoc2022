from dataclasses import dataclass
from typing import Callable
import math
from functools import reduce


@dataclass
class Monkey:
    items: 'list[int]'
    operation: 'Callable[[int], int]'
    test: 'int'
    if_true: int
    if_false: int

    _inspections: int = 0

    @staticmethod
    def parse_one():
        starting_items = input().rsplit(":", maxsplit=1)[1]
        _op = input().rsplit("=", maxsplit=1)[-1]
        test = input().rsplit(" ")[-1]
        if_true = input().split()[-1]
        if_false = input().split()[-1]
        return Monkey(
            list(map(int, starting_items.split(","))),
            lambda old: eval(_op.replace("old", str(old))),
            int(test),
            int(if_true),
            int(if_false)
        )

    def apply(self, item: int):
        self._inspections += 1
        return self.operation(item)


def main():
    monkeys: 'list[Monkey]' = []
    try:
        while True:
            input()
            monkeys.append(Monkey.parse_one())
            input()
    except EOFError:
        ...

    _mods = [m.test for m in monkeys]
    lcm = reduce(lambda x, y: (x*y) // math.gcd(x,y), _mods, 1)

    for round in range(10000):
        for m in monkeys:
            for i in m.items:
                i = m.apply(i) % lcm
                nxt = m.if_true if i % m.test == 0 else m.if_false
                monkeys[nxt].items.append(i)
            m.items.clear()  # cannot send to yourself

    counts = [m._inspections for m in monkeys]
    counts.sort(reverse=True)
    print(counts[0] * counts[1])


if __name__ == "__main__":
    main()
