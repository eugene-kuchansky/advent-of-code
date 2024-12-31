import sys


def read_data() -> tuple[list[list[int]], list[list[int]]]:
    raw_data = sys.stdin.read()
    keys = []
    locks = []
    for schematic in raw_data.strip().split("\n\n"):
        print(schematic)

        values = [-1] * 5
        add_to = keys
        for i, line in enumerate(schematic.split("\n")):
            if i == 0 and line == "#####":
                add_to = locks
            for j, shape in enumerate(line):
                if shape == "#":
                    values[j] += 1
        add_to.append(values)
    keys = sorted(keys, reverse=True)
    locks = sorted(locks)
    return keys, locks


def calc1(keys: list[list[int]], locks: list[list[int]]) -> int:
    result = 0
    for lock in locks:
        for key in keys:
            if all((lock[i] + key[i]) <= 5 for i in range(5)):
                result += 1

    return result


def calc2(keys: list[list[int]], locks: list[list[int]]) -> int:
    result = 0

    return result


if __name__ == "__main__":
    keys, locks = read_data()
    print(calc1(keys, locks))
    print(calc2(keys, locks))
