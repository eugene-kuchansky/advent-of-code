import sys
from typing import Iterable, List, NamedTuple, Set, Dict, Tuple
import re
from collections import defaultdict

Pos = Tuple[int, int]

DIRECTIONS: Dict[str, Pos] = {
    "se": (1, -1),
    "sw": (-1, -1),
    "nw": (-1, 1),
    "ne": (1, 1),
    "e": (2, 0),
    "w": (-2, 0),
}


class Move(NamedTuple):
    dx: int
    dy: int


def read_data(stream: Iterable[str]) -> List[List[Pos]]:
    paths = []
    for line in stream:
        line = line.strip()
        path = [DIRECTIONS[direction] for direction in re.findall("(se|sw|nw|ne|e|w)", line)]
        paths.append(path)
    return paths


def calc1(paths: List[List[Tuple[int, int]]]) -> Set[Pos]:
    blacks: Set[Pos] = set()

    for path in paths:
        x, y = (0, 0)
        for dx, dy in path:
            x += dx
            y += dy
        if (x, y) in blacks:
            blacks.remove((x, y))
        else:
            blacks.add((x, y))
    return blacks


def flip(prev_blacks: Set[Pos]) -> Set[Pos]:
    # if black:
    # if len(black_neighbours) == 0 or len(black_neighbours) > 2:
    # black -> white
    #
    # if white:
    # if len(black_neighbours) == 2:
    # white -> black
    new_blacks: Set[Pos] = set()

    whites: Dict[Pos, int] = defaultdict(int)
    for (x, y) in prev_blacks:
        black_neighbours = 0
        for dx, dy in DIRECTIONS.values():
            neighbour = (x + dx, y + dy)
            if neighbour in prev_blacks:
                black_neighbours += 1
            else:
                whites[neighbour] += 1
        if black_neighbours in (1, 2):
            new_blacks.add((x, y))

    for pos, black_neighbours_num in whites.items():
        if black_neighbours_num == 2:
            new_blacks.add(pos)

    return new_blacks


def calc2(blacks: Set[Pos]) -> int:
    for day in range(100):
        blacks = flip(blacks)
    return len(blacks)


if __name__ == "__main__":
    initial_paths = read_data(sys.stdin)

    black_pos = calc1(initial_paths)
    print(f"result 1: {len(black_pos)}")

    res2 = calc2(black_pos)
    print(f"result 2: {res2}")
