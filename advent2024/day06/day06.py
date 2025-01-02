import sys
from collections import defaultdict

DIRECTIONS = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}
TURN_RIGHT = {"north": "east", "east": "south", "south": "west", "west": "north"}


def read_data() -> tuple[dict[tuple[int, int], bool], int, tuple[int, int]]:
    raw_data = sys.stdin.read().strip()

    lab_map = defaultdict(lambda: False)
    max_size = len(raw_data.split("\n"))

    for y, line in enumerate(raw_data.split("\n")):
        for x, char in enumerate(line):
            if char == "^":
                start_pos = (x, y)
            elif char == "#":
                lab_map[(x, y)] = True

    return lab_map, max_size, start_pos


def calc1(lab_map: dict[tuple[int, int], bool], max_size: int, start_pos: tuple[int, int]) -> int:
    result = 0

    visited_positions = set()

    direction = "north"
    dx, dy = DIRECTIONS[direction]

    visited_positions.add(start_pos)
    x, y = start_pos

    while 0 <= y + dy < max_size and 0 <= x + dx < max_size:
        if lab_map[(x + dx, y + dy)]:
            direction = TURN_RIGHT[direction]
            dx, dy = DIRECTIONS[direction]
            continue

        x = x + dx
        y = y + dy
        visited_positions.add((x, y))

    result = len(visited_positions)
    return result


def is_cycle(x, y, direction, lab_map, max_size) -> bool:
    visited_positions = set()
    direction = TURN_RIGHT[direction]
    dx, dy = DIRECTIONS[direction]

    while 0 <= x + dx < max_size and 0 <= y + dy < max_size:
        if (x + dx, y + dy, direction) in visited_positions:
            return True

        if lab_map[(x + dx, y + dy)]:
            visited_positions.add((x, y, direction))
            direction = TURN_RIGHT[direction]
            dx, dy = DIRECTIONS[direction]
            continue

        visited_positions.add((x, y, direction))
        x, y = x + dx, y + dy

    return False


def calc2(lab_map: dict[tuple[int, int], bool], max_size: int, start_pos: tuple[int, int]) -> int:
    result = 0

    visited_positions = set()

    direction = "north"
    dx, dy = DIRECTIONS[direction]
    x, y = start_pos

    while 0 <= y + dy < max_size and 0 <= x + dx < max_size:
        if lab_map[(x + dx, y + dy)]:
            direction = TURN_RIGHT[direction]
            dx, dy = DIRECTIONS[direction]
            continue
        elif (x + dx, y + dy) not in visited_positions:
            # if we put a wall here
            lab_map[(x + dx, y + dy)] = True

            is_cycle_result = is_cycle(x, y, direction, lab_map, max_size)
            if is_cycle_result:
                result += 1
            lab_map[(x + dx, y + dy)] = False
        x = x + dx
        y = y + dy
        visited_positions.add((x, y))

    return result


if __name__ == "__main__":
    lab_map, max_size, start_pos = read_data()
    # print(calc1(lab_map, max_size, start_pos))
    print(calc2(lab_map, max_size, start_pos))
