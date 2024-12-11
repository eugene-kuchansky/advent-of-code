import sys


def to_int(x: str) -> int:
    try:
        return int(x)
    except ValueError:
        return 100


def read_data() -> list[list[int]]:
    raw_data = sys.stdin.read().strip()
    lines = []

    for line in raw_data.splitlines():
        lines.append([to_int(x) for x in line])

    return lines


def dfs(x: int, y: int, lava_map: list[list[int]]) -> list[tuple[int, int]]:
    value = lava_map[y][x]

    if lava_map[y][x] == 9:
        return [(x, y)]

    result = list()
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if 0 <= y + dy < len(lava_map) and 0 <= x + dx < len(lava_map[0]):
            next_value = lava_map[y + dy][x + dx]
            if next_value == value + 1:
                result.extend(dfs(x + dx, y + dy, lava_map))

    return result


def calc1(lava_map: list[list[int]]) -> int:
    result = 0
    destinations = 0
    for y, line in enumerate(lava_map):
        for x, place in enumerate(line):
            if place == 0:
                res = dfs(x, y, lava_map)
                destinations += len(set(res))

    result = destinations
    return result


def calc2(disk: list[int]) -> int:
    result = 0
    destinations = 0
    for y, line in enumerate(lava_map):
        for x, place in enumerate(line):
            if place == 0:
                res = dfs(x, y, lava_map)
                destinations += len(res)
    result = destinations
    return result


if __name__ == "__main__":
    lava_map = read_data()
    print(calc1(lava_map))
    print(calc2(lava_map))
