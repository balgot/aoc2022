import sys


def main():
    s = 0
    for line in sys.stdin:
        line = line.strip()
        l = len(line) // 2
        left, right = line[:l], line[l:]
        common = set(left).intersection(right)
        assert len(common) == 1, f"was {common}, {line}, {left}, {right}"

        c = common.pop()
        if c.islower():
            s += ord(c) - ord('a') + 1
        else:
            s += ord(c) - ord('A') + 27
    print(s)


if __name__ == "__main__":
    main()
