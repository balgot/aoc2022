import sys
from dataclasses import dataclass, field
from textwrap import dedent


@dataclass
class Data:
    name: str
    rate: int
    nxt: set


def main():
    data: 'list[Data]' = []
    for line in sys.stdin:
        _v, name, _h, _f, rate, _t, _l, _t, _v, *vs = line.split()
        rate = int(rate.strip(";").split("=")[-1])
        vs = { v.strip(",") for v in vs }
        data.append(Data(name, rate, vs))

    name2idx = {}
    for i, d in enumerate(data):
        name2idx[d.name] = i + 1

    print(dedent(f"""
    int N_VALVES = {len(data)};
    range Valves = 1..N_VALVES;

    Valve VALVES[Valves] = [
    """))
    for d in data:
        _s = "{ " + ", ".join(str(name2idx[nxt]) for nxt in d.nxt) + " }"
        print(f"\t<{d.rate}, {_s}>", end=",\n" if d != data[-1] else "\n")
    print("];")


if __name__ == "__main__":
    main()
