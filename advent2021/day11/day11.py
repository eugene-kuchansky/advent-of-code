from typing import List, Tuple
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

SIZE = 10
RELATIVE_NEIGHBORS_COORDS = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if not (x == 0 and x == 0)]
MAX_ENERGY = 9
INIT_ENERGY = 0


@dataclass
class Octopuses:
    energy: List[List[int]]

    def next_step(self) -> int:
        flashed = self._increase_all_by_one()
        flashes = len(flashed)

        while flashed:
            new_flashed = []
            for row, col in flashed:
                flashed_neighbors = self._increase_neighbors(row, col)
                new_flashed.extend(flashed_neighbors)
            flashed = new_flashed
            flashes += len(new_flashed)

        return flashes

    def _increase_all_by_one(self) -> List[Tuple[int, int]]:
        flashed: List[Tuple[int, int]] = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.energy[i][j] == MAX_ENERGY:
                    self.energy[i][j] = INIT_ENERGY
                    flashed.append((i, j))
                else:
                    self.energy[i][j] += 1
        return flashed

    def _increase_neighbors(self, row, col) -> List[Tuple[int, int]]:
        flashed: List[Tuple[int, int]] = []
        for n_row, n_col in self._neighbors(row, col):
            if self.energy[n_row][n_col] == MAX_ENERGY:
                self.energy[n_row][n_col] = INIT_ENERGY
                flashed.append((n_row, n_col))
            elif self.energy[n_row][n_col] != INIT_ENERGY:
                self.energy[n_row][n_col] += 1
        return flashed

    def _neighbors(self, row, col) -> List[Tuple[int, int]]:
        return [
            (row + dx, col + dy)
            for dx, dy in RELATIVE_NEIGHBORS_COORDS
            if SIZE > row + dx >= 0 and SIZE > col + dy >= 0
        ]


def parse(raw: str) -> Octopuses:
    return Octopuses([[int(energy) for energy in line] for line in raw.split("\n")])


def calc(octopuses: Octopuses) -> int:
    flashes = 0
    for step in range(100):
        flashes += octopuses.next_step()
    return flashes


def calc2(octopuses: Octopuses) -> int:
    step = 0
    all_octopuses_number = SIZE * SIZE
    while True:
        flashes = octopuses.next_step()
        step += 1
        # breaks on the step when all the octopus have flashed
        if flashes == all_octopuses_number:
            break
    return step


assert calc(parse(RAW)) == 1656
assert calc2(parse(RAW)) == 195


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data)))
    print(calc2(parse(raw_data)))
