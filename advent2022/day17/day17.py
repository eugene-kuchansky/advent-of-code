import sys
from typing import List, Tuple, Dict, NamedTuple, Optional
from dataclasses import dataclass, field
from itertools import cycle
from collections import defaultdict


@dataclass
class Shape:
    num: str
    shape: List[str]
    width: int = 0
    height: int = 0
    bottom: List = field(default_factory=list)
    top: List = field(default_factory=list)
    left: List = field(default_factory=list)
    right: List = field(default_factory=list)

    def __post_init__(self):
        self.width = len(self.shape[0])
        self.height = len(self.shape)
        self.top = [-1 for _ in range(len(self.shape[0]))]
        self.bottom = [-1 for _ in range(len(self.shape[0]))]

        for row_i, row in enumerate(self.shape):
            for col_i, value in enumerate(row):
                if self.top[col_i] == -1 and value == "@":
                    self.top[col_i] = row_i
        for row_i, row in enumerate(self.shape[::-1]):
            for col_i, value in enumerate(row):
                if self.bottom[col_i] == -1 and value == "@":
                    self.bottom[col_i] = len(self.shape) - row_i - 1

        self.right = [-1 for _ in range(len(self.shape))]
        self.left = [-1 for _ in range(len(self.shape))]

        for col_i in range(self.width):
            for row_i, row in enumerate(self.shape):
                if self.left[row_i] == -1 and self.shape[row_i][col_i] == "@":
                    self.left[row_i] = col_i
        for col_i in range(self.width - 1, -1, -1):
            for row_i, row in enumerate(self.shape):
                if self.right[row_i] == -1 and self.shape[row_i][col_i] == "@":
                    self.right[row_i] = col_i


SHAPES = [
    Shape("-", ["@@@@"]),
    Shape("+", [".@.", "@@@", ".@."]),
    Shape("L", ["..@", "..@", "@@@"]),
    Shape("I", ["@", "@", "@", "@"]),
    Shape("#", ["@@", "@@"]),
]


def read_data() -> List[str]:
    jets: List[str]
    raw_data = sys.stdin.read()
    jets = list(raw_data)

    return jets


POSITION_LEFT = 2
CHAMBER_WIDTH = 7
DISTANCE_TO_TOP = 3


class Coord(NamedTuple):
    col: int
    row: int


def get_max_height(chamber):
    if chamber:
        max_height = max(point.row for point in chamber)
    else:
        max_height = -1
    return max_height


def get_top_shape_profile(chamber, max_height):
    r = []
    for col in range(CHAMBER_WIDTH):
        try:
            col_max_height = max(point.row for point in chamber if point.col == col)
        except ValueError:
            col_max_height = -1
        r.append(max_height - col_max_height)
    return tuple(r)


def print_chamber(
    chamber: Dict[Coord, str],
    rock: Optional[Shape] = None,
    rock_row: Optional[int] = None,
    rock_col: Optional[int] = None,
):
    max_height = get_max_height(chamber) + 3

    if rock:
        max_height = rock_row + 1
    max_height = max(max_height, 4)

    rows = []
    rows.append(["-"] * CHAMBER_WIDTH)
    for row_i in range(max_height):
        row = []
        for col_i in range(CHAMBER_WIDTH):
            coord = Coord(col_i, row_i)
            point = chamber.get(coord, ".")
            if rock:
                if rock.width + rock_col - 1 >= col_i >= rock_col:
                    if rock_row >= row_i >= rock_row - rock.height + 1:
                        point = rock.shape[rock_row - row_i][col_i - rock_col]

            row.append(point)
        rows.append(row)

    for row in rows[::-1]:
        print(f"|{''.join(row)}|")
    print()


def move_rock_side(chamber: Dict[Coord, str], jet: str, rock: Shape, rock_row: int, rock_col: int) -> int:
    if jet == ">":
        if rock.width + rock_col == CHAMBER_WIDTH:
            return rock_col
        for j, right in enumerate(rock.right):
            row = rock_row - j
            col = rock_col + right
            if Coord(col + 1, row) in chamber:
                return rock_col
        return rock_col + 1
    else:
        if rock_col == 0:
            return rock_col
        for j, left in enumerate(rock.left):
            row = rock_row - j
            col = rock_col + left
            if Coord(col - 1, row) in chamber:
                return rock_col

        return rock_col - 1


def move_rock_down(chamber: Dict[Coord, str], rock: Shape, rock_row: int, rock_col: int) -> int:
    for i, bottom in enumerate(rock.bottom):
        col = rock_col + i
        row = rock_row - bottom
        if Coord(col, row - 1) in chamber or row - 1 == -1:
            return False
    return True


def get_wind(jets):
    jets_cycle = cycle(jets)
    i = 0
    while True:
        yield i, (next(jets_cycle))
        i += 1
        i = i % len(jets)


def detect_cycles(cache):
    for pattern in cache:
        if len(cache[pattern]) > 1:
            cycles = cache[pattern]
            break
    else:
        raise ValueError("cycle not found")
    cycle_start_step, max_height_start = cycles[0]
    cycle_next_step, max_height_next = cycles[1]
    return cycle_start_step, max_height_start, cycle_next_step - cycle_start_step, max_height_next - max_height_start


def go_tetris(jets: List[str], steps: int):
    chamber: Dict[Coord, str] = {}

    shapes_cycle = cycle(SHAPES)
    jets_cycle = get_wind(jets)
    cache = defaultdict(list)
    heights = []

    for step in range(steps):
        rock = next(shapes_cycle)
        rock_col = 2
        rock_row = get_max_height(chamber) + rock.height + DISTANCE_TO_TOP

        while True:
            jet_i, jet = next(jets_cycle)
            rock_col = move_rock_side(chamber, jet, rock, rock_row, rock_col)
            if move_rock_down(chamber, rock, rock_row, rock_col):
                rock_row -= 1
            else:
                break

        for i in range(rock.height):
            for j in range(rock.width):
                if rock.shape[i][j] == "@":
                    chamber[Coord(rock_col + j, rock_row - i)] = "#"

        max_height = get_max_height(chamber)
        heights.append(max_height)

        pattern = get_top_shape_profile(chamber, max_height)
        cache[(*pattern, jet_i, rock.num)].append((step, max_height))

    return get_max_height(chamber) + 1, cache, heights


def calc1(jets: List[str]) -> int:
    max_height, _, _ = go_tetris(jets, 2022)
    return max_height


def calc2(jets: List[str]) -> int:
    steps = 1000000000000
    _, cache, heights = go_tetris(jets, 2000)
    cycle_start_step, max_height_start, cycle_step, height_step = detect_cycles(cache)

    cycle_number, rest = divmod(steps - cycle_start_step, cycle_step)

    result = (
        max_height_start + cycle_number * height_step + (heights[cycle_start_step + rest] - heights[cycle_start_step])
    )

    return result


if __name__ == "__main__":
    data = read_data()
    # print(calc1(data))
    print(calc2(data))
