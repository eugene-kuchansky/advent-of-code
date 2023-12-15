import sys
from typing import List, Tuple


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[List[str]]:
    platform = []
    for line in lines:
        platform.append(list(line))
    return platform


def move(platform: List[List[str]]) -> List[List[str]]:
    # move all round rock to the north (top the top)
    # min_line is the position a rock could fall
    # at the beginning the rock could fall only to zero leven

    min_line = [0] * len(platform[0])
    for line_n, p in enumerate(platform):
        for i, rock in enumerate(p):
            if rock == "O":
                # this rock can fall
                # check where it can go to
                can_fall_to = min_line[i]
                # nothing can fall further than this rock
                min_line[i] = can_fall_to + 1
                # update rock position
                platform[line_n][i] = "."
                platform[can_fall_to][i] = "O"
            elif rock == "#":
                # this rock is square
                # nothing can fall further
                min_line[i] = line_n + 1
    return platform


def rotate_right(platform: List[List[str]]) -> List[List[str]]:
    # to fall to the top we can just rotate matrix if we need to fall to west (south, east)
    return [list(reversed(row)) for row in zip(*platform)]


def calc_loads(platform: List[List[str]]) -> int:
    result = 0
    for i, row in enumerate(reversed(platform)):
        result += row.count("O") * (i + 1)
    return result


def calc_hash(platform: List[List[str]]) -> Tuple[int]:
    # make a number to reflect positions of all round rocks
    # actually it's a tuple, but can be a string also
    # anything that can be hashed
    result = []
    for row in platform:
        cur_num = 0
        for j, rock in enumerate(row):
            if rock == "O":
                cur_num += 2**j
        result.append(cur_num)
    return tuple(result)


def calc1(platform: List[List[str]]) -> int:
    result = 0
    platform = move(platform)
    result = calc_loads(platform)
    return result


def make_cycle(platform: List[List[str]]) -> List[List[str]]:
    # move to the north, rotate to the right so west is new north, move, etc
    platform = move(platform)

    platform = rotate_right(platform)
    platform = move(platform)

    platform = rotate_right(platform)
    platform = move(platform)

    platform = rotate_right(platform)
    platform = move(platform)

    platform = rotate_right(platform)

    return platform


def calc2(platform: List[List[str]]) -> int:
    result = 0
    states = {}

    cycles_num = 1000000000
    initial_platform = [list(row) for row in platform]

    for i in range(cycles_num):
        # actually
        # we don't want to go thar far as 1000000000
        # we want to find num of the cycles when the position is the same as in some previous state
        # so cycle num of the first similar state is the beginning of the cycling
        # diff between first and second similar state it the cycle length
        platform = make_cycle(platform)
        state = calc_hash(platform)
        if state in states:
            cycle_num = i - states[state]
            cycle_start = states[state]
            break
        states[state] = i

    # we have to find what the phase would be at 1000000000 cycle
    # it can be done a bit more simple way
    # "platform" is already at first state of cycle start
    # so we don't have to start from initial state (zero cycle)
    # but anyway
    same_phase = (cycles_num - cycle_start) % cycle_num
    platform = initial_platform

    for i in range(cycle_start + same_phase):
        platform = make_cycle(platform)
        result = calc_loads(platform)

    return result


if __name__ == "__main__":
    raw_data = read_data()
    platform = parse(raw_data)
    print(calc1(platform))
    print(calc2(platform))
