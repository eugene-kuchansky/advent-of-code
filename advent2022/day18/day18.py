import sys
from typing import Dict
from dataclasses import dataclass

DELTAS = ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0))


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int


def read_data() -> Dict[Coord, str]:
    cubes = {}
    raw_data = sys.stdin.read()
    for cube_data in raw_data.split("\n"):
        x, y, z = cube_data.split(",")
        cubes[Coord(int(x), int(y), int(z))] = ""

    return cubes


def calc1(cubes: Dict[Coord, str]) -> int:
    result = 0
    for cube in cubes:
        for delta in DELTAS:
            coord = Coord(cube.x + delta[0], cube.y + delta[1], cube.z + delta[2])
            if coord not in cubes:
                result += 1
    return result


@dataclass
class Explore:
    cubes: Dict[Coord, str]
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def flood(self):
        start_flood = Coord(self.min_x, self.min_y, self.min_z)
        stack = [start_flood]
        filled = set([start_flood])
        touch_cubes = 0
        while stack:
            point = stack.pop()
            for delta in DELTAS:
                coord = Coord(point.x + delta[0], point.y + delta[1], point.z + delta[2])
                if coord in self.cubes:
                    touch_cubes += 1
                    continue
                if coord.x < self.min_x or coord.x > self.max_x:
                    continue
                if coord.y < self.min_y or coord.y > self.max_y:
                    continue
                if coord.z < self.min_z or coord.z > self.max_z:
                    continue
                if coord in filled:
                    continue
                stack.append(coord)
                filled.add(coord)
        return touch_cubes


def calc2(cubes: Dict[Coord, str]) -> int:
    result = 0
    x = [cube.x for cube in cubes]
    y = [cube.y for cube in cubes]
    z = [cube.z for cube in cubes]
    ex = Explore(cubes, min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1, min(z) - 1, max(z) + 1)
    result = ex.flood()
    return result


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
