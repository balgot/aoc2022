import sys


def stacks(lines: 'list[str]', n: int) -> 'list[list[str]]':
    result = [[] for _ in range(n)]
    lines = ["".join(x) for x in zip(*lines)]
    for i in range(n):
        stack = lines[1 + i*4]
        result[i].extend(reversed(stack.strip()))
    return result


def main():
    stack_lines = []
    st = None
    for line in sys.stdin:
        if "[" in line:
            stack_lines.append(line)
            continue
        if not st:
            assert "1" in line
            st = stacks(stack_lines, len(line.split()))
        elif line.startswith("move"):
            _move, n, _from, f, _to, t = line.split()
            n, f, t = map(int, (n, f, t))
            f -= 1
            t -= 1
            for i in reversed(range(n)):
                st[t].append(st[f][-i-1])
            for _ in range(n):
                st[f].pop()
    print("".join(s[-1] for s in st))


if __name__ == "__main__":
    main()
