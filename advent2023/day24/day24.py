import sys
from typing import List, NamedTuple
import functools
from itertools import chain
import sympy


class Hailstone(NamedTuple):
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @functools.cache
    def a(self):
        return self.dy / self.dx

    @functools.cache
    def c(self):
        return self.y - self.a() * self.x


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[Hailstone]:
    hailstones = []
    for line in lines:
        coords, dirs = line.split(" @ ")
        coords = [int(_) for _ in coords.split(", ")]
        dirs = [int(_) for _ in dirs.split(", ")]
        hailstones.append(Hailstone(coords[0], coords[1], coords[2], dirs[0], dirs[1], dirs[2]))

    return hailstones


def is_crossing(h1, h2, min_coord, max_coord) -> bool:
    # lines are parallel
    if h2.a() == h1.a():
        return False

    x = (h1.c() - h2.c()) / (h2.a() - h1.a())
    y = (h1.a() * h2.c() - h2.a() * h1.c()) / (h1.a() - h2.a())

    # outside the limits
    if x < min_coord or x > max_coord or y < min_coord or y > max_coord:
        return False

    # check if crossing is in the "past"
    # compare the crossing coord with speed (delta)
    if x < h1.x and h1.dx > 0 or x > h1.x and h1.dx < 0:
        return False
    if y < h1.y and h1.dy > 0 or y > h1.y and h1.dy < 0:
        return False

    # and for the second one
    if x < h2.x and h2.dx > 0 or x > h2.x and h2.dx < 0:
        return False
    if y < h2.y and h2.dy > 0 or y > h2.y and h2.dy < 0:
        return False

    return True


def find_crossed(hailstones: List[Hailstone], min_coord: int, max_coord: int) -> int:
    crossed_num = 0
    for i, h1 in enumerate(hailstones[:-1]):
        for h2 in hailstones[i + 1 :]:
            crossed_num += int(is_crossing(h1, h2, min_coord, max_coord))
    return crossed_num


def calc1(hailstones: List[Hailstone]) -> int:
    # result = find_crossed(hailstones, min_coord=7, max_coord=27)
    result = find_crossed(hailstones, min_coord=200000000000000, max_coord=400000000000000)
    return result


def find_magic_rock_coords(hailstones: List[Hailstone]) -> int:
    # find *approximate* possible speed range
    speeds = list(chain.from_iterable(((abs(h.dx), abs(h.dy), abs(h.dz)) for h in hailstones)))
    max_speed = max(speeds) * 2
    min_speed = -max_speed

    d_speed = {
        "dx": set(),
        "dy": set(),
        "dz": set(),
    }
    d_coord = {
        "dx": "x",
        "dy": "y",
        "dz": "z",
    }

    for direction in d_speed:
        # let's find two hailstones with same speed by x,y, or z axis
        hailstones_sorted = sorted(hailstones, key=lambda h: getattr(h, direction))
        for i, h1 in enumerate(hailstones_sorted[:-1]):
            h2 = hailstones_sorted[i + 1]
            speed1 = getattr(h1, direction)
            speed2 = getattr(h2, direction)

            if speed1 == speed2:
                # if they are moving in the same speed
                # them the distance between them should be covered with some speed
                # that speed should be integer value
                # it might be several speed values for one pair of hailstones
                # so we need to find common speeds for all pairs
                coord1 = getattr(h1, d_coord[direction])
                coord2 = getattr(h2, d_coord[direction])

                diff = coord1 - coord2
                possible_speeds = set()

                for speed in range(min_speed, max_speed):
                    if speed == speed1 or not speed:
                        continue
                    if diff % (speed - speed1) == 0:
                        possible_speeds.add(speed)
                if not d_speed[direction]:
                    d_speed[direction] = possible_speeds
                else:
                    d_speed[direction] = d_speed[direction].intersection(possible_speeds)

                if len(d_speed[direction]) == 1:
                    break

    dx = d_speed["dx"].pop()
    dy = d_speed["dy"].pop()
    dz = d_speed["dz"].pop()

    # take 2 first hailstones and intersect with found line
    x1, y1, z1, dx1, dy1, dz1 = hailstones[0]
    x2, y2, z2, dx2, dy2, dz2 = hailstones[1]

    x, y, z, t1, t2 = sympy.symbols("x y z t1 t2")
    system_eq = (
        sympy.Eq(x + dx * t1, x1 + dx1 * t1),
        sympy.Eq(y + dy * t1, y1 + dy1 * t1),
        sympy.Eq(z + dz * t1, z1 + dz1 * t1),
        sympy.Eq(x + dx * t2, x2 + dx2 * t2),
        sympy.Eq(y + dy * t2, y2 + dy2 * t2),
        sympy.Eq(z + dz * t2, z2 + dz2 * t2),
    )
    # solving the system of equations
    solution = sympy.solve(system_eq, (x, y, z, t1, t2))

    x_coord = solution[x]
    y_coord = solution[y]
    z_coord = solution[z]
    return x_coord + y_coord + z_coord


def calc2(hailstones: List[Hailstone]) -> int:
    result = find_magic_rock_coords(hailstones)
    return result


if __name__ == "__main__":
    raw_data = read_data()
    hailstones = parse(raw_data)
    print(calc1(hailstones))
    print(calc2(hailstones))
