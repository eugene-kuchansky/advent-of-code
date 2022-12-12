from typing import List, Dict
from dataclasses import dataclass, field


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

MAP_SIZE = 9


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Vent:
    start: Point
    end: Point


@dataclass
class Diagram:
    points: Dict[Point, int] = field(default_factory=dict)

    def add_vent(self, vent: Vent):
        d_x = 0
        d_y = 0
        if vent.start.x < vent.end.x:
            d_x = 1
        elif vent.start.x > vent.end.x:
            d_x = -1
        if vent.start.y < vent.end.y:
            d_y = 1
        elif vent.start.y > vent.end.y:
            d_y = -1
        x = vent.start.x
        y = vent.start.y
        self._add_point(Point(x, y))

        while vent.end.x != x or vent.end.y != y:
            x += d_x
            y += d_y
            self._add_point(Point(x, y))

    def _add_point(self, point: Point):
        if point in self.points:
            self.points[point] += 1
        else:
            self.points[point] = 1

    def draw(self):
        for y in range(MAP_SIZE + 1):
            for x in range(MAP_SIZE + 1):
                point = Point(x, y)
                print(self.points.get(point, "."), end="")
            print()

    def calc_overlap(self):
        return sum(1 for overlaps in self.points.values() if overlaps > 1)


def parse1(raw: str) -> List[Vent]:
    vents = []
    for line in raw.split("\n"):
        if not line:
            continue
        start, end = line.split(" -> ")
        start_x, start_y = start.split(",")
        end_x, end_y = end.split(",")
        if start_x == end_x or start_y == end_y:
            vents.append(Vent(Point(int(start_x), int(start_y)), Point(int(end_x), int(end_y))))
    return vents


def parse2(raw: str) -> List[Vent]:
    vents = []
    for line in raw.split("\n"):
        if not line:
            continue
        start, end = line.split(" -> ")
        start_x, start_y = start.split(",")
        end_x, end_y = end.split(",")
        vents.append(Vent(Point(int(start_x), int(start_y)), Point(int(end_x), int(end_y))))

    return vents


def create_diagram(vents: List[Vent]) -> int:
    diagram = Diagram()
    for vent in vents:
        diagram.add_vent(vent)
    diagram.draw()
    return diagram.calc_overlap()


assert create_diagram(parse1(RAW)) == 5
assert create_diagram(parse2(RAW)) == 12

if __name__ == "__main__":
    raw_data = read_data()
    print(create_diagram(parse1(raw_data)))
    print(create_diagram(parse2(raw_data)))
