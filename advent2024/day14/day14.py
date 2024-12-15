import sys
from collections import namedtuple

# useless stupid data structures
# we don't need them
Point = namedtuple("Point", ["x", "y"])
Velocity = namedtuple("Velocity", ["vx", "vy"])


def read_data() -> tuple[list[Point], list[Velocity]]:
    raw_data = sys.stdin.read()
    positions = []
    velocities = []
    for line in raw_data.strip().splitlines():
        p, v = line.split(" ")
        x, y = p[2:].split(",")
        vx, vy = v[2:].split(",")
        positions.append(Point(int(x), int(y)))
        velocities.append(Velocity(int(vx), int(vy)))
    return positions, velocities


def move_robot(position: Point, velocity: Velocity, width: int, height: int, time: int) -> Point:
    return Point((position.x + velocity.vx * time) % width, (position.y + velocity.vy * time) % height)


def danger_level(coords: list[Point], width: int, height: int) -> int:
    quadrants = [
        [0, width // 2, 0, height // 2],
        [width // 2 + 1, width, 0, height // 2],
        [0, width // 2, height // 2 + 1, height],
        [width // 2 + 1, width, height // 2 + 1, height],
    ]
    level = 1
    for x1, x2, y1, y2 in quadrants:
        in_quadrant = 0
        for point in coords:
            if x1 <= point.x < x2 and y1 <= point.y < y2:
                in_quadrant += 1
        level *= in_quadrant
    return level


def calc1(positions: list[Point], velocities: list[Velocity]) -> int:
    result = 0

    width = 101
    height = 103
    coords = list()
    for position, velocity in zip(positions, velocities):
        coords.append(move_robot(position, velocity, width=width, height=height, time=100))

    quadrants = [
        [0, width // 2, 0, height // 2],
        [width // 2 + 1, width, 0, height // 2],
        [0, width // 2, height // 2 + 1, height],
        [width // 2 + 1, width, height // 2 + 1, height],
    ]
    result = 1
    for x1, x2, y1, y2 in quadrants:
        in_quadrant = 0
        for point in coords:
            if x1 <= point.x < x2 and y1 <= point.y < y2:
                in_quadrant += 1
        result *= in_quadrant
    return result


def display(coords: list[Point], width: int, height: int):
    for y in range(height):
        for x in range(width):
            if Point(x, y) in coords:
                print("#", end="")
            else:
                print(".", end="")
        print()


def calc2(positions: list[Point], velocities: list[Velocity]) -> int:
    result = 0
    width = 101
    height = 103
    min_danger = 10000000000000000

    for sec in range(10000):
        coords = list()
        for position, velocity in zip(positions, velocities):
            coords.append(move_robot(position, velocity, width=width, height=height, time=1))

        positions = coords
        # there was a hint in part 1
        # we need to find the minimum danger level
        level = danger_level(coords, width, height)
        if level < min_danger:
            min_danger = level
            tree_coords = coords.copy()
            result = sec + 1

    display(tree_coords, width, height)

    return result


if __name__ == "__main__":
    positions, velocities = read_data()
    print(calc1(positions, velocities))
    print(calc2(positions, velocities))
