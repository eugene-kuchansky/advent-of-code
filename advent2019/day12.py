from math import gcd
from typing import List, Tuple, Dict
from itertools import combinations


initial_position = """<x=-6, y=2, z=-9>
<x=12, y=-14, z=-4>
<x=9, y=5, z=-6>
<x=-1, y=-4, z=9>"""


PLANET_NUM = 4
COORDS = ["x", "y", "z"]


def read_positions(initial_position: str) -> Dict[str, List[int]]:
    coord_positions = {
        "x": [],
        "y": [],
        "z": [],
    }
    planets = initial_position.split("\n")
    for planet in planets:
        p = [int(val.split("=")[1]) for val in planet.strip("<>").split(",")]
        coord_positions["x"].append(p[0])
        coord_positions["y"].append(p[1])
        coord_positions["z"].append(p[2])
    return coord_positions


def init_positions() -> Dict[str, List[int]]:
    return {
        "x": [0 for _ in range(PLANET_NUM)],
        "y": [0 for _ in range(PLANET_NUM)],
        "z": [0 for _ in range(PLANET_NUM)],
    }


def calc_velocity(v1: int, v2: int) -> Tuple[int, int]:
    delta1 = 0
    delta2 = 0
    if v1 > v2:
        delta1, delta2 = -1, 1
    elif v1 < v2:
        delta1, delta2 = 1, -1
    return delta1, delta2


def apply_gravity(velocities: List[int], positions: List[int]) -> List[int]:
    speed_delta: List[List[int]] = [
        [] for _ in range(PLANET_NUM)
    ]
    for planet1, planet2 in combinations(range(PLANET_NUM), 2):
        delta1, delta2 = calc_velocity(positions[planet1], positions[planet2])
        speed_delta[planet1].append(delta1)
        speed_delta[planet2].append(delta2)

    new_velocities: List[int] = []

    for planet in range(PLANET_NUM):
        velocity = velocities[planet]
        new_velocity = velocity + sum(delta for delta in speed_delta[planet])
        new_velocities.append(new_velocity)
    return new_velocities


def apply_velocity(velocities: List[int], positions: List[int]) -> List[int]:
    new_positions = []
    for position, velocity in zip(positions, velocities):
        new_position = position + velocity
        new_positions.append(new_position)
    return new_positions


def calc_energy(x: int, y: int, z: int) -> int:
    return sum(abs(_) for _ in (x, y, z))


def calc_total_energy(velocities: Dict[str, List[int]], positions: Dict[str, List[int]]) -> None:
    energy = 0
    for planet in range(PLANET_NUM):
        energy += calc_energy(*[velocities[coord][planet] for coord in COORDS]) * \
                  calc_energy(*[positions[coord][planet] for coord in COORDS])
    print(energy)


def show(coord_positions, coord_velocities):
    for planet in range(PLANET_NUM):
        print(
            "pos (x=", coord_positions["x"][planet],
            "y=", coord_positions["y"][planet],
            "z=", coord_positions["z"][planet],
            end=") "
        )
        print(
            "vel (x=", coord_velocities["x"][planet],
            "y=", coord_velocities["y"][planet],
            "z=", coord_velocities["z"][planet],
            end=")\n"
        )


def main1():
    coord_positions = read_positions(initial_position)
    coord_velocities = init_positions()

    print("step", 0)
    show(coord_positions, coord_velocities)

    for _ in range(1000):
        for coord in COORDS:
            coord_velocities[coord] = apply_gravity(coord_velocities[coord], coord_positions[coord])
            coord_positions[coord] = apply_velocity(coord_velocities[coord], coord_positions[coord])
        print("step", _ + 1)

    show(coord_positions, coord_velocities)
    calc_total_energy(coord_velocities, coord_positions)


def find_match(coord_velocities, coord_positions, velocities0, positions0):
    step = 0
    while True:
        step += 1
        coord_velocities = apply_gravity(coord_velocities, coord_positions)
        coord_positions = apply_velocity(coord_velocities, coord_positions)
        if coord_velocities == velocities0 and coord_positions == positions0:
            break
    return step


# def gcd(a, b):
#     while b:
#         a, b = b, a % b
#     return a
#

def lcm(a, b):
    return a * b // gcd(a, b)


def main2():
    coord_positions = read_positions(initial_position)
    coord_velocities = init_positions()

    show(coord_positions, coord_velocities)

    positions0 = coord_positions.copy()
    velocities0 = coord_velocities.copy()
    steps = []
    for coord in COORDS:
        step = find_match(coord_velocities[coord], coord_positions[coord], velocities0[coord], positions0[coord])
        steps.append(step)
        print(coord, step)

    res = lcm(lcm(steps[0], steps[1]), steps[2])
    print(res)
    #show(coord_positions, coord_velocities)


if __name__ == "__main__":
    main2()


