from dataclasses import dataclass
from typing import Callable


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
        return self.operation(item) // 3


def main():
    monkeys: 'list[Monkey]' = []
    try:
        while True:
            input()
            monkeys.append(Monkey.parse_one())
            input()
    except EOFError:
        ...

    for round in range(20):
        for m in monkeys:
            for i in m.items:
                i = m.apply(i)
                nxt = m.if_true if i % m.test == 0 else m.if_false
                monkeys[nxt].items.append(i)
            m.items.clear()  # cannot send to yourself

    counts = [m._inspections for m in monkeys]
    counts.sort(reverse=True)
    print(counts[0] * counts[1])


if __name__ == "__main__":
    main()
