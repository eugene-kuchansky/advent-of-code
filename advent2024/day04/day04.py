import sys


def read_data() -> dict[tuple[int, int], str]:
    raw_data = sys.stdin.read()

    field = {}

    for y, line in enumerate(raw_data.split("\n")):
        if not line:
            continue
        for x, char in enumerate(line):
            field[(x, y)] = char

    return field


def check_position(field: dict[tuple[int, int], str], x: int, y: int) -> int:
    # search for X M A S
    result = 0
    search_list = ["X", "M", "A", "S"]

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue

            for i, char in enumerate(search_list):
                if field.get((x + dx * i, y + dy * i)) != char:
                    break
            else:
                result += 1

    return result


def check_xmas(field: dict[tuple[int, int], str], x: int, y: int) -> int:
    # search for M A S in shape of X
    if field[(x, y)] != "A":
        return 0

    search_list = ["M", "S"]

    c1 = (x - 1, y - 1)
    c2 = (x + 1, y + 1)
    if not ([field.get(c1), field.get(c2)] == search_list or [field.get(c1), field.get(c2)] == search_list[::-1]):
        return 0

    c3 = (x - 1, y + 1)
    c4 = (x + 1, y - 1)
    if not ([field.get(c3), field.get(c4)] == search_list or [field.get(c3), field.get(c4)] == search_list[::-1]):
        return 0

    return 1


def calc1(field: dict[tuple[int, int], str]):
    result = 0

    for coord in field:
        result += check_position(field, coord[0], coord[1])
    return result


def calc2(field: dict[tuple[int, int], str]):
    result = 0

    for coord in field:
        result += check_xmas(field, coord[0], coord[1])

    return result


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
