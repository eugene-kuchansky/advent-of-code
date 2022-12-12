from typing import Tuple, List, Set
from dataclasses import dataclass
import heapq


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

Point = Tuple[int, int]

RELATIVE_NEIGHBORS_COORDS: List[Point] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


@dataclass
class Carven:
    map: List[List[int]]
    nr: int = 0
    nc: int = 0

    def __post_init__(self):
        self.nr = len(self.map)
        self.nc = len(self.map[0])

    def find_lowers_path(self) -> int:
        visited: Set[Point] = set()
        # priority queue
        risks_of_positions: List[Tuple[int, Point]] = []
        # is point already in priority queue
        risk_calculated = set()

        row = col = 0
        current_risk = 0

        while True:
            visited.add((row, col))

            for n_row, n_col in self.neighbors(row, col):
                if (n_row, n_col) in visited:
                    continue

                if (n_row, n_col) not in risk_calculated:
                    risk = current_risk + self.map[n_row][n_col]
                    heapq.heappush(risks_of_positions, (risk, (n_row, n_col)))
                    risk_calculated.add((n_row, n_col))

            current_risk, (row, col) = heapq.heappop(risks_of_positions)

            if (row, col) == (self.nr - 1, self.nc - 1):
                break

        return current_risk

    def neighbors(self, row, col) -> List[Point]:
        neighbors = []
        for dr, dc in RELATIVE_NEIGHBORS_COORDS:
            new_row, new_col = row + dr, col + dc
            if self.nr > new_row >= 0 and self.nc > new_col >= 0:
                neighbors.append((new_row, new_col))
        return neighbors


def parse(raw: str) -> Carven:
    return Carven([[int(_) for _ in line] for line in raw.splitlines()])


def parse2(raw: str) -> Carven:
    initial_grid = [[int(_) for _ in line] for line in raw.splitlines()]

    nr = len(initial_grid)
    nc = len(initial_grid[0])

    def get_initial_value(new_row, new_col):
        row = new_row % nr
        col = new_col % nr
        incr_row = new_row // nr
        incr_col = new_col // nc
        total = (initial_grid[row][col] + incr_row + incr_col) % 9
        if total == 0:
            total = 9
        return total

    final_grid = [[get_initial_value(row, col) for col in range(nc * 5)] for row in range(nr * 5)]
    return Carven(final_grid)


def calc(carven: Carven) -> int:
    return carven.find_lowers_path()


assert calc(parse(RAW)) == 40
assert calc(parse2(RAW)) == 315


if __name__ == "__main__":
    raw = read_data()
    print(calc(parse(raw)))
    print(calc(parse2(raw)))
