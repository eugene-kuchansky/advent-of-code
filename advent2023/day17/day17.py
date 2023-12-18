import sys
from typing import List, NamedTuple, Dict, Tuple
import heapq


class Coord(NamedTuple):
    x: int
    y: int


NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

OPPOSITE_DIR = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

ALL_DIRS = [
    (EAST, 1, 0),
    (SOUTH, 0, 1),
    (NORTH, 0, -1),
    (WEST, -1, 0),
]


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Dict[Coord, str]:
    heat_map = {}
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            heat_map[Coord(x, y)] = int(symbol)
    return heat_map


def get_directions(coord: Coord, from_dir: str, max_step: int) -> List[List[Tuple[str, Coord, int]]]:
    all_dirs = []

    for to_dir, dx, dy in ALL_DIRS:
        if to_dir == OPPOSITE_DIR[from_dir] or to_dir == from_dir:
            continue
        dirs = []
        for i in range(1, max_step):
            dirs.append((to_dir, Coord(coord.x + dx * i, coord.y + dy * i), i))
        all_dirs.append(dirs)
    return all_dirs


def search_path(heat_map: Dict[Coord, str], min_step: int, max_step: int) -> int:
    max_x = max(coord.x for coord in heat_map)
    max_y = max(coord.y for coord in heat_map)
    end_coord = Coord(max_x, max_y)

    q: List[Tuple[int, Coord, str, int]] = []

    coord = Coord(0, 0)
    heat_loss = 0
    same_dir_steps = 0

    q.append((heat_loss, coord, EAST, same_dir_steps))
    q.append((heat_loss, coord, SOUTH, same_dir_steps))

    visited = set()

    while q:
        heat_loss, coord, curr_dir, same_dir_steps = heapq.heappop(q)

        if coord == end_coord:
            return heat_loss

        if (coord, curr_dir) in visited:
            continue
        visited.add((coord, curr_dir))

        for dirs in get_directions(coord, curr_dir, max_step):
            new_heat_loss = heat_loss
            for new_curr_dir, new_coord, new_same_dir_steps in dirs:
                if new_coord not in heat_map:
                    continue

                new_heat_loss = new_heat_loss + heat_map[new_coord]

                if new_same_dir_steps < min_step:
                    continue

                if (new_coord, new_curr_dir) in visited:
                    continue
                heapq.heappush(q, (new_heat_loss, new_coord, new_curr_dir, new_same_dir_steps))

    raise Exception("nowhere to go")


def calc1(heat_map: Dict[Coord, int]) -> int:
    result = search_path(heat_map, 1, 4)
    return result


def calc2(heat_map: Dict[Coord, int]) -> int:
    result = search_path(heat_map, 4, 11)
    return result


if __name__ == "__main__":
    raw_data = read_data()
    contraption = parse(raw_data)
    print(calc1(contraption))
    print(calc2(contraption))
