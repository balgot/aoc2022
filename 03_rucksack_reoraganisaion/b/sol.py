import sys


def main():
    sol = 0
    lines = list(map(str.strip, sys.stdin))

    for i in range(0, len(lines), 3):
        f, s, t = lines[i], lines[i+1], lines[i+2]
        common = set(f).intersection(s).intersection(t)
        assert len(common) == 1, f"was {common}, {f}, {s}, {t}"

        c = common.pop()
        if c.islower():
            sol += ord(c) - ord('a') + 1
        else:
            sol += ord(c) - ord('A') + 27
    print(sol)


if __name__ == "__main__":
    main()
