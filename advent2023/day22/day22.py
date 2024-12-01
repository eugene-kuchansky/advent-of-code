import sys
from typing import List, NamedTuple, Dict, Set
from collections import defaultdict
from dataclasses import dataclass


class Coord(NamedTuple):
    x: int
    y: int


@dataclass
class Brick:
    id: int
    left: Coord
    right: Coord
    bottom: int
    top: int

    def __hash__(self) -> int:
        return hash(self.id)


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Dict[Coord, str]:
    bricks = []
    for i, line in enumerate(lines):
        side1, side2 = line.split("~")
        bottom_side = [int(_) for _ in side1.split(",")]
        top_side = [int(_) for _ in side2.split(",")]
        bottom, top = bottom_side[2], top_side[2]
        if bottom > top:
            bottom, top = top, bottom
        left = Coord(bottom_side[0], bottom_side[1])
        right = Coord(top_side[0], top_side[1])
        if left[0] > right[0]:
            left, right = right, left
        bricks.append(Brick(i, left, right, bottom, top))
    bricks = sorted(bricks, key=lambda b: b.bottom)
    return bricks


def fall_down(bricks: List[Brick]) -> List[Brick]:
    floor = {}
    for brick in bricks:
        coords = []
        for x in range(brick.left.x, brick.right.x + 1):
            for y in range(brick.left.y, brick.right.y + 1):
                coord = Coord(x, y)
                coords.append(coord)
        min_height = max([floor.get(coord, 0) for coord in coords]) + 1
        adjust = brick.bottom - min_height
        brick.bottom -= adjust
        brick.top -= adjust
        for coord in coords:
            floor[coord] = brick.top
    return bricks


def have_intersection(brick1: Brick, brick2: Brick) -> bool:
    if (
        brick1.right.x < brick2.left.x
        or brick2.right.x < brick1.left.x
        or brick1.right.y < brick2.left.y
        or brick2.right.y < brick1.left.y
    ):
        return False
    return True


def non_safe_disintegrate(bricks: List[Brick]) -> Set[int]:
    bottom_at = defaultdict(list)
    top_at = defaultdict(list)
    for brick in bricks:
        bottom_at[brick.bottom].append(brick)
        top_at[brick.top + 1].append(brick)

    unsafe_bricks = set()
    for bottom, check_bricks in bottom_at.items():
        if bottom == 1:
            continue
        support_bricks = top_at[bottom]

        for brick in check_bricks:
            supported_by = []
            for support in support_bricks:
                if have_intersection(brick, support):
                    supported_by.append(support.id)
            if len(supported_by) == 1:
                unsafe_bricks.add(supported_by[0])

    return unsafe_bricks


def dependencies(brick, top_at: Dict[int, Set[int]], bricks_dependencies: Dict[int, Set[int]]):
    if brick in bricks_dependencies:
        return
    deps = []
    supporters_ids = []
    path = set()

    for lower_brick in top_at[brick.bottom - 1]:
        if have_intersection(brick, lower_brick):
            dependencies(lower_brick, top_at, bricks_dependencies)
            deps.append(bricks_dependencies[lower_brick.id])
            supporters_ids.append(lower_brick.id)
    if len(deps) == 1:
        path = set(deps[0])
        path.add(supporters_ids[0])
    elif deps:
        path = set.intersection(*deps)

    bricks_dependencies[brick.id] = set(path)


def all_fallen_bricks(bricks: List[Brick], unsafe_bricks: Set[int]) -> int:
    bottom_at = defaultdict(list)
    top_at = defaultdict(list)

    for brick in bricks:
        bottom_at[brick.bottom].append(brick)
        top_at[brick.top].append(brick)

    bricks_dependencies: Dict[int, List[List[int]]] = {}

    for brick in bricks:
        dependencies(brick, top_at, bricks_dependencies)
    return sum(len(_) for _ in bricks_dependencies.values())


def calc1(bricks: List[Brick]) -> int:
    bricks = fall_down(bricks)
    unsafe_bricks = non_safe_disintegrate(bricks)
    result = len(bricks) - len(unsafe_bricks)
    return result


def calc2(bricks: List[Brick]) -> int:
    bricks = fall_down(bricks)
    unsafe_bricks = non_safe_disintegrate(bricks)
    result = all_fallen_bricks(bricks, unsafe_bricks)
    return result


if __name__ == "__main__":
    raw_data = read_data()
    bricks = parse(raw_data)
    print(calc1(bricks))
    bricks = parse(raw_data)
    print(calc2(bricks))
