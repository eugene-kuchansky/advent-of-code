from typing import List, Set, Dict, FrozenSet, Tuple
from dataclasses import dataclass, field
from heapq import nlargest


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """2199943210
3987894921
9856789892
8767896789
9899965678"""

MAX_HEIGHT = 9


@dataclass
class Floor:
    heights: List[List[int]]
    row_len: int = field(init=False)
    col_len: int = field(init=False)

    def __post_init__(self):
        self.col_len = len(self.heights[0])
        self.row_len = len(self.heights)

    def find_low_points(self) -> List[int]:
        return [self.heights[row][col] for row, col in self._find_low_points_coords()]

    def _find_low_points_coords(self) -> List[Tuple[int, int]]:
        low_points = []
        for row in range(self.row_len):
            for col in range(self.col_len):
                if self._is_lower(row, col):
                    low_points.append((row, col))
        return low_points

    def _is_lower(self, row: int, col: int) -> bool:
        height = self.heights[row][col]
        for n_row, n_col in self._get_neighbors_coords(row, col):
            if height >= self.heights[n_row][n_col]:
                return False
        return True

    def _get_neighbors_coords(self, row, col) -> List[Tuple[int, int]]:
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.row_len - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.col_len - 1:
            neighbors.append((row, col + 1))
        return neighbors

    def find_basins(self) -> List[int]:
        basils = []
        for row, col in self._find_low_points_coords():
            basil = self._find_basil(row, col, visited=set())
            basils.append(basil)
        return basils

    def _find_basil(self, row: int, col: int, visited: Set) -> int:
        if (row, col) in visited:
            return 0
        if self.heights[row][col] == MAX_HEIGHT:
            return 0

        total = 1
        visited.add((row, col))
        for n_row, n_col in self._get_neighbors_coords(row, col):
            total += self._find_basil(n_row, n_col, visited)

        return total


def parse(raw: str) -> Floor:
    return Floor([[int(col) for col in line] for line in raw.split("\n")])


def calc(floor: Floor) -> int:
    return sum(low_point + 1 for low_point in floor.find_low_points())


def calc2(floor: Floor) -> int:
    prod = 1
    for basin in nlargest(3, floor.find_basins()):
        prod *= basin
    return prod


assert calc(parse(RAW)) == 15
assert calc2(parse(RAW)) == 1134
# assert calc2(parse(RAW)) == 61229
# assert calc2(parse(RAW2)) == 5353


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data)))
    print(calc2(parse(raw_data)))
