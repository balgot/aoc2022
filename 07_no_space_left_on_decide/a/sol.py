import sys
from dataclasses import dataclass, field


@dataclass
class File:
    is_file: bool
    name: str
    parent: 'File | None' = None
    size: int = 0
    children: 'list[File]' = field(default_factory=list)


def postorder(root: File):
    if root.is_file:
        return
    total_size = 0
    for c in root.children:
        postorder(c)
        total_size += c.size
    root.size = total_size

def filter_out(root, max_size):
    if root.is_file:
        return 0

    total = root.size if root.size <= max_size else 0
    for c in root.children:
        total += filter_out(c, max_size)
    return total

def pprint(root, indent=""):
    _desc = f"file, size={root.size}" if root.is_file else "dir"
    print(f"{indent}- {root.name} ({_desc})")
    for c in root.children:
        pprint(c, indent+"  ")


def main():
    root: 'File' = File(False, "/")
    pwd: 'None | File' = None
    for line in sys.stdin:
        if not line.startswith("$"):
            assert pwd is not None
            fst, snd = line.strip().split()
            if fst == "dir":
                pwd.children.append(File(False, snd, pwd))
            else:
                pwd.children.append(File(True, snd, pwd, int(fst)))
        else:
            _, cmd, *args = line.strip().split()
            if cmd == "cd":
                if args[0] == "/":
                    pwd = root
                elif args[0] == "..":
                    pwd = pwd.parent or pwd
                else:
                    for c in pwd.children:
                        if c.name == args[0]:
                            pwd = c
                            break
                    else:
                        assert False

    postorder(root)
    print(filter_out(root, 100000))
    # pprint(root)



if __name__ == "__main__":
    main()