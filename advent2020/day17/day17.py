import sys
from typing import Iterable, Set, Tuple, Iterator, Callable

ACTIVE = "#"
INACTIVE = "."


def neighbors3(cube: Tuple) -> Iterator[Tuple]:
    # this dead simple way of generation possible neighbours is a more faster than this one:
    # for deltas in itertools.product([-1, 0, 1], repeat=4):
    #     if not any(deltas):
    #         continue
    #     yield x + deltas[0], y + deltas[1], z + deltas[2]

    x, y, z = cube
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == dy == dz == 0:
                    continue
                yield x + dx, y + dy, z + dz


def neighbors4(cube: Tuple) -> Iterator[Tuple]:
    x, y, z, w = cube
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx == dy == dz == dw == 0:
                        continue
                    yield x + dx, y + dy, z + dz, w + dw


def read_data(stream: Iterable[str]) -> Set[Tuple]:
    actives = set()

    for y, line in enumerate(stream):
        for x, place in enumerate(line):
            if place == ACTIVE:
                actives.add((x, y, 0))
    return actives


def boot_cycle(actives: Set[Tuple], neighbors: Callable) -> Set[Tuple]:
    next_actives: Set[Tuple] = set()
    checked_inactives: Set[Tuple] = set()

    for cube in actives:
        active_num = 0
        for neighbor in neighbors(cube):
            if neighbor in actives:
                active_num += 1
            else:
                if neighbor in checked_inactives:
                    continue
                # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                # Otherwise, the cube remains inactive.
                inactive_num = 0
                for inactive_neighbor in neighbors(neighbor):
                    if inactive_neighbor in actives:
                        inactive_num += 1
                if inactive_num == 3:
                    next_actives.add(neighbor)
                checked_inactives.add(neighbor)

        # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
        # Otherwise, the cube becomes inactive.
        if 3 >= active_num >= 2:
            next_actives.add(cube)

    return next_actives


def calc1(actives: Set[Tuple]) -> int:
    # neighbors_gen = Neighbors(3)
    for i in range(6):
        actives = boot_cycle(actives, neighbors3)
    return len(actives)


def calc2(actives3: Set[Tuple]) -> int:
    actives = {(cube[0], cube[1], cube[2], 0) for cube in actives3}
    # neighbors_gen = Neighbors(4)
    for i in range(6):
        actives = boot_cycle(actives, neighbors4)
    return len(actives)


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
