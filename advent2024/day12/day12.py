import sys


def read_data() -> list[list[str]]:
    raw_data = sys.stdin.read().strip()
    plots = []

    for line in raw_data.split("\n"):
        plots.append(list(line))

    return plots


def explore(plots: list[list[str]], x: int, y: int) -> tuple[set[tuple[int, int]], dict[str, list[tuple[int, int]]]]:
    area = set()
    perimeter = {
        "top": [],
        "bottom": [],
        "left": [],
        "right": [],
    }
    plant = plots[y][x]
    current = [(x, y)]

    # kinda bfs
    while current:
        new_current = []
        for x, y in current:
            if (x, y) in area:
                continue
            # remember all plants in region
            area.add((x, y))
            # check all sides
            for dx, dy, side in [(0, 1, "top"), (1, 0, "right"), (0, -1, "bottom"), (-1, 0, "left")]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in area:
                    continue
                if 0 <= nx < len(plots[0]) and 0 <= ny < len(plots) and plots[ny][nx] == plant:
                    # this is plan
                    new_current.append((nx, ny))
                else:
                    # this is perimeter
                    perimeter[side].append((nx, ny))
        current = new_current

    return area, perimeter


def calc1(plots: list[list[str]]) -> int:
    result = 0
    all_plots = set()
    for y, row in enumerate(plots):
        for x, plot in enumerate(row):
            if (x, y) in all_plots:
                continue
            area, perimeter = explore(plots, x, y)
            perimeter_count = sum(len(v) for v in perimeter.values())
            all_plots.update(area)
            result += perimeter_count * len(area)
    return result


def get_sides(perimeter: dict[str, list[tuple[int, int]]]) -> int:
    sides = 0
    variants = [
        ("top", 1, 0),
        ("bottom", 1, 0),
        ("right", 0, 1),
        ("left", 0, 1),
    ]
    # check all sides
    for direction, dx, dy in variants:
        side_x = None
        side_y = None
        # take vertical sides, sort by x
        # this is one side while x is the same, and vertical is monotone (+1)
        # take horizontal sides, sort by y
        # this is one side while y is the same, and horizontal is monotone (+1)
        for x, y in sorted(perimeter[direction], key=lambda coord: (coord[dx], coord[dy])):
            if side_x is None or side_y is None:
                side_x = x
                side_y = y
                sides += 1
            elif side_x != x - dx or side_y != y - dy:
                side_x = x
                side_y = y
                sides += 1
            else:
                side_x = x
                side_y = y

    return sides


def calc2(plots: list[list[str]]) -> int:
    result = 0
    all_plots = set()
    for y, row in enumerate(plots):
        for x, plot in enumerate(row):
            if (x, y) in all_plots:
                continue

            area, perimeter = explore(plots, x, y)
            sides = get_sides(perimeter)
            all_plots.update(area)
            result += sides * len(area)

    return result


if __name__ == "__main__":
    plots = read_data()
    print(calc1(plots))
    print(calc2(plots))
