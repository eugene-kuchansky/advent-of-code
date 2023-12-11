import sys
from typing import List, NamedTuple


class Coord(NamedTuple):
    x: int
    y: int


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[Coord]:
    galaxies = []
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == "#":
                galaxies.append(Coord(x, y))

    return galaxies


def get_distance(start, end, lines):
    if end < start:
        start, end = end, start
    distance = sum([lines[_] for _ in range(start, end)])
    return distance


def calc_distance(galaxy_1: Coord, galaxy_2: Coord, x_lines: List[int], y_lines: List[int]) -> int:
    # total manhattan distance is dx + dy
    x_distance = get_distance(galaxy_1.x, galaxy_2.x, x_lines)
    y_distance = get_distance(galaxy_1.y, galaxy_2.y, y_lines)
    return x_distance + y_distance


def get_corrected_line(coords: List[int], empty_distance: int) -> List[int]:
    # get all galaxies coordinates x or y
    all_galaxies_coords = set(coords)

    # get the dimension of the map
    max_coord = max(all_galaxies_coords) + 1

    # calc the real distance of the line (increase if no galaxies at that line)
    lines = [1 if x in all_galaxies_coords else empty_distance for x in range(max_coord)]
    return lines


def calc_pair_distances(galaxies: List[Coord], empty_distance: int) -> int:
    result = 0

    x_lines = get_corrected_line([coord.x for coord in galaxies], empty_distance)
    y_lines = get_corrected_line([coord.y for coord in galaxies], empty_distance)

    # calc pairwise distances
    for i, galaxy_1 in enumerate(galaxies[:-1]):
        for galaxy_2 in galaxies[i + 1 :]:
            result += calc_distance(galaxy_1, galaxy_2, x_lines, y_lines)

    return result


def calc1(galaxies: List[Coord]) -> int:
    return calc_pair_distances(galaxies, empty_distance=2)


def calc2(galaxies: List[Coord]) -> int:
    return calc_pair_distances(galaxies, empty_distance=1000000)


if __name__ == "__main__":
    raw_data = read_data()
    galaxies = parse(raw_data)
    print(calc1(galaxies))
    print(calc2(galaxies))
