import sys
from typing import List, NamedTuple, Dict, Set


class Coord(NamedTuple):
    x: int
    y: int


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Dict[Coord, str]:
    heat_map = {}
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            heat_map[Coord(x, y)] = symbol
    return heat_map


def is_inside(coord: Coord, garden_size: int) -> bool:
    return garden_size > coord.x >= 0 and garden_size > coord.y >= 0


def take_steps(start_coord: Coord, rocks: Set[Coord], garden_size: int, steps: int, include_start: bool) -> int:
    if steps == 0:
        return 0
    next_reached_coords = [set(), set([start_coord])]

    start_ind = int(include_start)

    if include_start:
        steps -= 1

    for _ in range(steps):
        new_reached = set()
        for coord in next_reached_coords[-1]:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                new_coord = Coord(coord.x + dx, coord.y + dy)
                if is_inside(new_coord, garden_size) and new_coord not in rocks:
                    new_reached.add(new_coord)
        new_reached = new_reached - next_reached_coords[-2]
        next_reached_coords.append(new_reached)

    all_reached_coords = set.union(*[end_steps for end_steps in next_reached_coords[start_ind::2]])
    return len(all_reached_coords)


def calc_total_area(start_coord: Coord, rocks: Set[Coord], garden_size: int, steps: int) -> int:
    # this is number of gardens to reach for each direction: up, down, left right
    r = steps // garden_size
    # starting point - half of the size
    middle = garden_size // 2

    # there will be some number of completely covered gardens
    # some of them are odd, some - even
    # the calculation is empiric, just draw and you'll see
    # we start with even
    even_gardens_num = (r - 1) ** 2

    # number of odds gardens is bigger
    odd_gardens_num = r**2

    # it doesn't matter how to fill them, so let's fill from center point
    # we need to cover the garden completely so number of steps is
    even_complete_garden_steps = take_steps(start_coord, rocks, garden_size, steps=garden_size * 2, include_start=False)
    odd_complete_garden_steps = take_steps(start_coord, rocks, garden_size, steps=garden_size * 2, include_start=True)

    right_peak_gardner_steps = take_steps(Coord(0, middle), rocks, garden_size, steps=garden_size, include_start=True)
    left_peak_gardner_steps = take_steps(
        Coord(garden_size - 1, middle), rocks, garden_size, steps=garden_size, include_start=True
    )
    bottom_peak_gardner_steps = take_steps(Coord(middle, 0), rocks, garden_size, steps=garden_size, include_start=True)
    top_peak_gardner_steps = take_steps(
        Coord(middle, garden_size - 1), rocks, garden_size, steps=garden_size, include_start=True
    )

    left_top_triangle = take_steps(
        Coord(garden_size - 1, garden_size - 1), rocks, garden_size, steps=middle, include_start=True
    )
    right_top_triangle = take_steps(Coord(0, garden_size - 1), rocks, garden_size, steps=middle, include_start=True)
    left_bottom_triangle = take_steps(Coord(garden_size - 1, 0), rocks, garden_size, steps=middle, include_start=True)
    right_bottom_triangle = take_steps(Coord(0, 0), rocks, garden_size, steps=middle, include_start=True)

    left_top_pentagon = take_steps(
        Coord(garden_size - 1, garden_size - 1),
        rocks,
        garden_size,
        steps=garden_size // 2 + garden_size,
        include_start=False,
    )

    right_top_pentagon = take_steps(
        Coord(0, garden_size - 1),
        rocks,
        garden_size,
        steps=garden_size // 2 + garden_size,
        include_start=False,
    )

    left_bottom_pentagon = take_steps(
        Coord(garden_size - 1, 0),
        rocks,
        garden_size,
        steps=garden_size // 2 + garden_size,
        include_start=False,
    )

    right_bottom_pentagon = take_steps(
        Coord(0, 0), rocks, garden_size, steps=garden_size // 2 + garden_size, include_start=False
    )

    result = 0

    result += even_complete_garden_steps * even_gardens_num
    result += odd_complete_garden_steps * odd_gardens_num

    result += right_peak_gardner_steps
    result += left_peak_gardner_steps
    result += bottom_peak_gardner_steps
    result += top_peak_gardner_steps

    result += r * left_top_triangle
    result += r * right_top_triangle
    result += r * left_bottom_triangle
    result += r * right_bottom_triangle

    result += (r - 1) * left_top_pentagon
    result += (r - 1) * right_top_pentagon
    result += (r - 1) * left_bottom_pentagon
    result += (r - 1) * right_bottom_pentagon

    return result


def calc1(garden: Dict[Coord, str]) -> int:
    start_coord = next(coord for coord, symbol in garden.items() if symbol == "S")
    rocks = set([coord for coord, symbol in garden.items() if symbol == "#"])

    garden_size = max(coord.x for coord in garden) + 1

    result = take_steps(start_coord, rocks, garden_size, steps=65, include_start=True)

    return result


def calc2(garden: Dict[Coord, str]) -> int:
    start_coord = next(coord for coord, symbol in garden.items() if symbol == "S")
    rocks = set([coord for coord, symbol in garden.items() if symbol == "#"])

    garden_size = max(coord.x for coord in garden) + 1

    result = calc_total_area(start_coord, rocks, garden_size, steps=26501365)
    return result


if __name__ == "__main__":
    raw_data = read_data()
    garden = parse(raw_data)
    print(calc1(garden))
    # print(calc2(garden))
