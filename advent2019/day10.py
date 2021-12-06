from typing import List
from collections import namedtuple, defaultdict
from fractions import Fraction
from operator import itemgetter
from time import time


asteroid_map = """.#..#..#..#...#..#...###....##.#....
.#.........#.#....#...........####.#
#..##.##.#....#...#.#....#..........
......###..#.#...............#.....#
......#......#....#..##....##.......
....................#..............#
..#....##...#.....#..#..........#..#
..#.#.....#..#..#..#.#....#.###.##.#
.........##.#..#.......#.........#..
.##..#..##....#.#...#.#.####.....#..
.##....#.#....#.......#......##....#
..#...#.#...##......#####..#......#.
##..#...#.....#...###..#..........#.
......##..#.##..#.....#.......##..#.
#..##..#..#.....#.#.####........#.#.
#......#..........###...#..#....##..
.......#...#....#.##.#..##......#...
.............##.......#.#.#..#...##.
..#..##...#...............#..#......
##....#...#.#....#..#.....##..##....
.#...##...........#..#..............
.............#....###...#.##....#.#.
#..#.#..#...#....#.....#............
....#.###....##....##...............
....#..........#..#..#.......#.#....
#..#....##.....#............#..#....
...##.............#...#.....#..###..
...#.......#........###.##..#..##.##
.#.##.#...##..#.#........#.....#....
#......#....#......#....###.#.....#.
......#.##......#...#.#.##.##...#...
..#...#.#........#....#...........#.
......#.##..#..#.....#......##..#...
..##.........#......#..##.#.#.......
.#....#..#....###..#....##..........
..............#....##...#.####...##."""


Point = namedtuple("Point", ["x", "y"])


class Line(object):
    def __init__(self, p1: Point, p2: Point) -> None:
        self.is_vertical = bool(p1.x == p2.x)
        self.is_horizontal = bool(p1.y == p2.y)
        self.p1 = p1
        self.p2 = p2
        self.slope = None
        if not (self.is_vertical or self.is_horizontal):
            self.slope = Fraction(self.p1.y - self.p2.y, self.p1.x - self.p2.x)

    def in_line(self, p3: Point) -> bool:
        if self.is_vertical:
            return p3.x == self.p1.x
        elif self.is_horizontal:
            return p3.y == self.p1.y
        if self.p1.x == p3.x or self.p1.y == p3.y:
            return False
        return self.slope == Fraction(self.p1.y - p3.y, self.p1.x - p3.x)

    def is_closer(self, p3: Point) -> bool:
        if self.p1.x > self.p2.x:
            x1 = self.p1.x
            x2 = self.p2.x
        else:
            x2 = self.p1.x
            x1 = self.p2.x
        if self.p1.y > self.p2.y:
            y1 = self.p1.y
            y2 = self.p2.y
        else:
            y2 = self.p1.y
            y1 = self.p2.y
        return x1 >= p3.x >= x2 and y1 >= p3.y >= y2

    def in_between(self, p3: Point) -> bool:
        return self.in_line(p3) and self.is_closer(p3)


def read_map(raw_map: str) -> List[Point]:
    points = []
    for y, line in enumerate(raw_map.split("\n")):
        for x, item in enumerate(line):
            if item == "#":
                point = Point(x, y)
                points.append(point)
    return points


def calc(points: List[Point]):
    connections = defaultdict(int)
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            line = Line(points[i], points[j])
            is_connected = True
            for k in range(i + 1, j):
                if line.in_between(points[k]):
                    is_connected = False
                    break
            if is_connected:
                connections[points[i]] += 1
                connections[points[j]] += 1

    res = max(((point, conn) for point, conn in connections.items()), key=itemgetter(1))
    print(res)


TOP = 0
TOP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
TOP_LEFT = 7


def create_directions(items_map: List[Point], station: Point) -> List[List[Point]]:
    directions = [
        {0: []},  # TOP
        {},  # TOP_RIGHT
        {0: []},  # RIGHT
        {},  # DOWN_RIGHT
        {0: []},  # DOWN
        {},  # DOWN_LEFT
        {0: []},  # LEFT
        {},  # TOP_LEFT
    ]
    for point in items_map:
        if point == station:
            continue
        distance = (point.x - station.x) ** 2 + (point.y - station.y) ** 2

        if point.y < station.y:
            # asteroid is higher
            if point.x == station.x:
                direction = TOP
                slope = 0
            elif point.x > station.x:
                direction = TOP_RIGHT
                slope = Fraction(station.x - point.x, point.y - station.y)
            else:
                direction = TOP_LEFT
                slope = Fraction(station.y - point.y, station.x - point.x)
        elif point.y > station.y:
            # asteroid is lower
            if point.x == station.x:
                direction = DOWN
                slope = 0
            elif point.x > station.x:
                direction = DOWN_RIGHT
                slope = Fraction(point.y - station.y, point.x - station.x)
            else:
                direction = DOWN_LEFT
                slope = Fraction(station.x - point.x, point.y - station.y)
        else:
            # same level
            if point.x > station.x:
                direction = RIGHT
                slope = 0
            else:
                direction = LEFT
                slope = 0

        if slope not in directions[direction]:
            directions[direction][slope] = []
        directions[direction][slope].append((distance, point))
    sorted_directions = []

    for dir, sector in enumerate(directions):
        slopes = sorted(sector.keys())
        for slope in slopes:
            asteroids = sector[slope]
            sorted_asteroids = [point for _, point in sorted(asteroids, key=itemgetter(0))]
            sorted_directions.append(sorted_asteroids)

    return sorted_directions


def fire(directions: List[List[Point]]) -> None:
    shoot = 0
    do_shoot = True
    while do_shoot:
        for asteroids in directions:
            if asteroids:
                p = asteroids.pop(0)
                shoot += 1
                if shoot == 200:
                    do_shoot = False
                    return p
                    break


def main():
    # t = time()
    items_map = read_map(asteroid_map)
    #calc(items_map)
    # print(time() - t)
    station = Point(x=17, y=22)
    # station = Point(x=11, y=13)
    directions = create_directions(items_map, station)
    p = fire(directions)
    print(p.x * 100 + p.y)


main()

def test():
    items_map = [
        Point(0, -1),  # top

        Point(1, -3),  # first top right
        Point(3, -1),  # second --

        Point(1, 0),  # right

        Point(3, 1),  # first bottom right
        Point(1, 3),  # second --

        Point(0, 1),  # bottom

        Point(-1, 3),  # first bottom left
        Point(-3, 1),  # second

        Point(-1, 0),  # left

        Point(-3, -1),  # first top left
        Point(-1, -3),  # second --


    ]
    station = Point(0, 0)
    directions = create_directions(items_map, station)
    # test = [
    #     [Point(0, -1), ],  # top
    #     [Point(1, -3), ],  # first top right
    #     [Point(3, -1), ],  # second --
    #     [Point(1, 0), ],  # right
    #     [Point(3, 1), ],  # first bottom right
    #     [Point(1, 3), ],  # second --
    #     [Point(0, 1), ],  # bottom
    #     [Point(-1, 3), ],  # first bottom left
    #     [Point(-3, 1), ],  # second
    #     [Point(-1, -3), ],  # first bottom left
    #     [Point(-3, -1), ],  # second
    #     [Point(-1, 0), ],  # left
    #     [Point(-3, -1), ],  # first top left
    #     [Point(-1, -3), ],  # second --
    # ]
    test = [[_] for _ in items_map]
    assert test == directions

