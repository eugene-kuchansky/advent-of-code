from typing import Set, Dict, Tuple, List
from collections import namedtuple

Pos = namedtuple("Pos", "x y")

SIZE = 5
MIDDLE = SIZE // 2
ADJACENT = (Pos(0, -1), Pos(0, 1), Pos(-1, 0), Pos(1, 0))


def get_inners() -> Dict[Pos, List[Pos]]:
    left_inner = Pos(MIDDLE - 1, MIDDLE)
    right_inner = Pos(MIDDLE + 1, MIDDLE)
    top_inner = Pos(MIDDLE, MIDDLE - 1)
    bottom_inner = Pos(MIDDLE, MIDDLE + 1)

    inners = {
        left_inner: [Pos(0, y) for y in range(5)],
        right_inner: [Pos(SIZE - 1, y) for y in range(5)],
        top_inner: [Pos(x, 0) for x in range(5)],
        bottom_inner: [Pos(x, SIZE - 1) for x in range(5)]
    }
    return inners


def get_outers(inners: Dict[Pos, List[Pos]]) -> Dict[Pos, List[Pos]]:
    outers = {}
    for inner_pos, outers_pos in inners.items():
        for outer_pos in outers_pos:
            if outer_pos not in outers:
                outers[outer_pos] = []
            outers[outer_pos].append(inner_pos)
    return outers


INNERS = get_inners()
OUTERS = get_outers(INNERS)


def read_data() -> Set[Pos]:
    with open("input_data/24.txt") as f:
        raw_data = f.read()

    bugs = set()
    lines = raw_data.strip().split("\n")
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile == "#":
                bugs.add(Pos(x, y))
    return bugs


def is_outside(tile: Pos) -> bool:
    return not ((SIZE > tile.x >= 0) and (SIZE > tile.y >= 0))


def check_neighbours(item: Pos, bugs: Set[Pos]) -> Tuple[int, Set[Pos]]:
    neighbours_num = 0
    empty_to_check = set()

    for direction in ADJACENT:
        neighbour = Pos(item.x + direction.x, item.y + direction.y)
        if is_outside(neighbour):
            continue
        if neighbour in bugs:
            neighbours_num += 1
        else:
            empty_to_check.add(neighbour)

    return neighbours_num, empty_to_check


def get_next_gen(bugs) -> Set[Pos]:
    next_bugs = set()
    empty_to_check = set()

    for bug in bugs:
        neighbours_num, neighbour_empties = check_neighbours(bug, bugs)
        if neighbours_num == 1:
            next_bugs.add(bug)
        empty_to_check = empty_to_check.union(neighbour_empties)

    for tile in empty_to_check:
        neighbours_num, _ = check_neighbours(tile, bugs)
        if 2 >= neighbours_num >= 1:
            next_bugs.add(tile)

    return next_bugs


def hash_bugs(bugs):
    return tuple(sorted(list(bugs)))


def get_other_level_adjacent(item: Pos, level_num: int) -> Set[Tuple[int, Pos]]:
    if item in INNERS:
        to_check = INNERS[item]
    elif item in OUTERS:
        to_check = OUTERS[item]
    else:
        raise RuntimeError(f"{item} is not adjacent to inner")

    return {(level_num, pos) for pos in to_check}


def get_neighbours(item: Pos, level_num: int) -> Set[Tuple[int, Pos]]:
    adjacent = set()
    for direction in ADJACENT:
        neighbour = Pos(item.x + direction.x, item.y + direction.y)
        if neighbour.x == neighbour.y == MIDDLE:
            # check inner
            other_level_adjacent = get_other_level_adjacent(item, level_num + 1)
            adjacent = adjacent.union(other_level_adjacent)
        elif is_outside(neighbour):
            # check outer
            other_level_adjacent = get_other_level_adjacent(item, level_num - 1)
            adjacent = adjacent.union(other_level_adjacent)
        else:
            adjacent.add((level_num, neighbour))

    return adjacent


def check_neighbours_level(item: Pos, level_num: int, levels: Dict[int, Set[Pos]]) -> Tuple[int, Set[Tuple[int, Pos]]]:
    neighbours_num = 0
    empty_to_check = set()

    for n_level_num, neighbour in get_neighbours(item, level_num):
        if neighbour in levels.get(n_level_num, set()):
            neighbours_num += 1
        else:
            empty_to_check.add((n_level_num, neighbour))
    return neighbours_num, empty_to_check


def print_level(bugs):
    for y in range(SIZE):
        for x in range(SIZE):
            if Pos(x, y) in bugs:
                if x == y == MIDDLE:
                    print("bug!")
                    exit()
                print("#", end="")
            elif x == y == MIDDLE:
                print("?", end="")
            else:
                print(".", end="")
        print()


def print_levels(levels: Dict[int, Set[Pos]]):
    for level_num, bugs in levels.items():
        print(f"Level: {level_num}")
        print_level(bugs)
        print()


def get_next_gen_levels(levels: Dict[int, Set[Pos]]) -> Dict[int, Set[Pos]]:
    next_levels: Dict[int, Set[Pos]] = dict()
    empty_to_check: Set[Tuple[int, Pos]] = set()

    for level_num, bugs in levels.items():
        next_bugs = set()
        for bug in bugs:
            neighbours_num, neighbour_empties = check_neighbours_level(bug, level_num, levels)
            if neighbours_num == 1:
                next_bugs.add(bug)
            empty_to_check = empty_to_check.union(neighbour_empties)

        next_levels[level_num] = next_bugs

    for level_num, tile in empty_to_check:
        neighbours_num, _ = check_neighbours_level(tile, level_num, levels)
        if 2 >= neighbours_num >= 1:
            if level_num not in next_levels:
                next_levels[level_num] = set()
            next_levels[level_num].add(tile)

    return next_levels


def calc1():
    layouts = set()
    bugs = read_data()
    layouts.add(hash_bugs(bugs))

    while True:
        bugs = get_next_gen(bugs)
        bugs_hash = hash_bugs(bugs)
        if bugs_hash in layouts:
            break
        layouts.add(bugs_hash)

    res = sum(pow(2, y * SIZE + x) for (x, y) in bugs)
    return res


def calc2():
    levels: Dict[int, Set[Pos]] = dict()
    bugs = read_data()
    levels[0] = bugs

    for _ in range(200):
        levels = get_next_gen_levels(levels)

    res = sum(len(bugs) for bugs in levels.values())
    return res


if __name__ == "__main__":
    print("res1:", calc1())
    print("res2:", calc2())
