import sys
from typing import List, NamedTuple, Dict, Tuple
from collections import defaultdict, deque
from functools import cache


class Coord(NamedTuple):
    x: int
    y: int


NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

EMPTY_ENC = "."
W_SPLITTER = "|"
H_SPLITTER = "-"

MIRROR_B_SLASH = "\\"
MIRROR_SLASH = "/"


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Dict[Coord, str]:
    contraption = {}
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            contraption[Coord(x, y)] = symbol
    return contraption


def to_east(coord):
    return EAST, Coord(coord.x + 1, coord.y)


def to_west(coord):
    return WEST, Coord(coord.x - 1, coord.y)


def to_north(coord):
    return NORTH, Coord(coord.x, coord.y - 1)


def to_south(coord):
    return SOUTH, Coord(coord.x, coord.y + 1)


def empty_dir(beam_dir: str, coord: Coord) -> List[Tuple[str, Coord]]:
    """
    this is "." just move on
    """
    directions = {
        EAST: to_east,
        WEST: to_west,
        NORTH: to_north,
        SOUTH: to_south,
    }
    return [directions[beam_dir](coord)]


def b_slash_dir(beam_dir: str, coord: Coord) -> List[Tuple[str, Coord]]:
    """
    this is \
    reflects beam
    """
    directions = {
        EAST: to_south,
        WEST: to_north,
        NORTH: to_west,
        SOUTH: to_east,
    }
    return [directions[beam_dir](coord)]


def slash_dir(beam_dir: str, coord: Coord) -> List[Tuple[str, Coord]]:
    """
    this is /
    reflects beam
    """
    directions = {
        EAST: to_north,
        WEST: to_south,
        NORTH: to_east,
        SOUTH: to_west,
    }
    return [directions[beam_dir](coord)]


def h_split_dir(beam_dir: str, coord: Coord) -> List[Tuple[str, Coord]]:
    """
    this is -
    split beams from NORTH and SOUTH
    """
    if beam_dir in (NORTH, SOUTH):
        return [to_east(coord), to_west(coord)]

    return empty_dir(beam_dir, coord)


def w_split_dir(beam_dir: str, coord: Coord) -> List[Tuple[str, Coord]]:
    """
    this is |
    split beams from EAST and WEST
    """
    if beam_dir in (EAST, WEST):
        return [to_north(coord), to_south(coord)]

    return empty_dir(beam_dir, coord)


@cache
def get_beams(beam_dir: str, coord: Coord, encounter: str) -> List[Tuple[str, Coord]]:
    if beam_dir not in (EAST, WEST, NORTH, SOUTH):
        raise ValueError("incorrect direction", beam_dir)

    possible_encounters = {
        EMPTY_ENC: empty_dir,
        MIRROR_B_SLASH: b_slash_dir,
        MIRROR_SLASH: slash_dir,
        W_SPLITTER: w_split_dir,
        H_SPLITTER: h_split_dir,
    }

    return possible_encounters[encounter](beam_dir, coord)


def travel_light(start_dir: str, start_coord: Coord, contraption: Dict[Coord, str]) -> Dict[Coord, Tuple[str]]:
    visited: Dict[Coord, Tuple[str]] = defaultdict(set)
    visited[start_coord].add(start_dir)

    beams = deque()
    beams.append((start_coord, start_dir))

    while beams:
        coord, beam_dir = beams.popleft()

        for new_dir, new_coord in get_beams(beam_dir, coord, contraption[coord]):
            if new_coord not in contraption:
                continue
            if new_dir in visited[new_coord]:
                continue
            visited[new_coord].add(new_dir)
            beams.append((new_coord, new_dir))

    return visited


def calc1(contraption: Dict[Coord, str]) -> int:
    start_dir = EAST
    start_coord = Coord(0, 0)

    visited_coords = travel_light(start_dir, start_coord, contraption)

    return len(visited_coords)


def calc2(contraption: Dict[Coord, str]) -> int:
    max_x = max(coord.x for coord in contraption)
    max_y = max(coord.y for coord in contraption)

    # from top
    start_dir = SOUTH
    max_top = 0
    for x in range(max_x + 1):
        start_coord = Coord(x, 0)

        visited_coords = travel_light(start_dir, start_coord, contraption)
        max_top = max(max_top, len(visited_coords))

    # from bottom
    start_dir = NORTH
    max_bottom = 0
    for x in range(max_x + 1):
        start_coord = Coord(x, max_y)

        visited_coords = travel_light(start_dir, start_coord, contraption)
        max_bottom = max(max_bottom, len(visited_coords))

    # from left
    start_dir = EAST
    max_left = 0
    for y in range(max_y + 1):
        start_coord = Coord(0, y)

        visited_coords = travel_light(start_dir, start_coord, contraption)
        max_left = max(max_left, len(visited_coords))

    # from right
    start_dir = WEST
    max_right = 0
    for y in range(max_y + 1):
        start_coord = Coord(max_x, y)

        visited_coords = travel_light(start_dir, start_coord, contraption)
        max_right = max(max_right, len(visited_coords))

    return max(max_top, max_bottom, max_left, max_right)


if __name__ == "__main__":
    raw_data = read_data()
    contraption = parse(raw_data)
    print(calc1(contraption))
    print(calc2(contraption))
