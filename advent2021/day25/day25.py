from typing import List, Tuple, Set
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


@dataclass
class Cucumbers:
    max_col: int
    max_row: int
    coords: Set[Tuple[int, int]]
    step: Tuple[int, int]

    def move(self, other_cucumbers: "Cucumbers") -> "Cucumbers":
        coords = set()
        for old_coord in self.coords:
            coord = self._new_coord(old_coord)
            if coord in self.coords or coord in other_cucumbers.coords:
                coord = old_coord
            coords.add(coord)
        return Cucumbers(self.max_col, self.max_row, coords, self.step)

    def _new_coord(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        new_row, new_col = coord[0] + self.step[0], coord[1] + self.step[1]
        if new_row == self.max_row:
            new_row = 0
        if new_col == self.max_col:
            new_col = 0
        return new_row, new_col


def parse(raw: str) -> Tuple[Cucumbers, Cucumbers]:
    lines = raw.splitlines()
    max_row = len(lines)
    max_col = len(lines[0])

    east_cucumbers: List[Tuple[int, int]] = []
    south_cucumbers: List[Tuple[int, int]] = []
    for row, line in enumerate(lines):
        for col, something in enumerate(line):
            if something == ">":
                east_cucumbers.append((row, col))
            elif something == "v":
                south_cucumbers.append((row, col))

    return (
        Cucumbers(max_col, max_row, set(east_cucumbers), step=(0, 1)),
        Cucumbers(max_col, max_row, set(south_cucumbers), step=(1, 0)),
    )


def draw(east_cucumbers, south_cucumbers):
    for row in range(east_cucumbers.max_row):
        for col in range(east_cucumbers.max_col):
            if (row, col) in east_cucumbers.coords:
                print(">", end="")
            elif (row, col) in south_cucumbers.coords:
                print("v", end="")
            else:
                print(".", end="")
        print()


def calc(east_cucumbers: Cucumbers, south_cucumbers) -> int:
    step = 1
    while True:
        new_east_cucumbers = east_cucumbers.move(south_cucumbers)
        new_south_cucumbers = south_cucumbers.move(new_east_cucumbers)

        if new_east_cucumbers.coords == east_cucumbers.coords and new_south_cucumbers.coords == south_cucumbers.coords:
            break

        step += 1
        east_cucumbers = new_east_cucumbers
        south_cucumbers = new_south_cucumbers
    return step


RAW = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

assert calc(*parse(RAW)) == 58

if __name__ == "__main__":
    raw = read_data()
    print(calc(*parse(raw)))

