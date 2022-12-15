import sys
from typing import NamedTuple, Dict


class Coord(NamedTuple):
    x: int
    y: int


def read_data() -> Dict[Coord, str]:
    raw_data = sys.stdin.read()
    cave: Dict[Coord, str] = {}
    for lines in raw_data.split("\n"):
        points = [[int(point) for point in point_data.split(",")] for point_data in lines.split(" -> ")]
        from_point = points[0]
        for to_point in points[1:]:
            dx = to_point[0] - from_point[0]
            dy = to_point[1] - from_point[1]
            if dy == 0:
                # vertical line
                start_x = from_point[0] if dx > 0 else to_point[0]
                for i in range(abs(dx) + 1):
                    x = start_x + i
                    y = from_point[1]
                    cave[Coord(x, y)] = "#"
            else:
                # horizontal line
                start_y = from_point[1] if dy > 0 else to_point[1]
                for i in range(abs(dy) + 1):
                    y = start_y + i
                    x = from_point[0]
                    cave[Coord(x, y)] = "#"
            from_point = to_point
    return cave


def calc1(cave: Dict[Coord, str]) -> int:
    sands = 0

    start = Coord(500, 0)
    path = [start]
    lowest_y = max([point.y for point in cave])
    falling_away = False

    while True:
        pos = path[-1]
        can_fall = True
        while can_fall and not falling_away:
            down_pos = Coord(pos.x, pos.y + 1)
            left_pos = Coord(pos.x - 1, pos.y + 1)
            right_pos = Coord(pos.x + 1, pos.y + 1)
            for new_pos in (down_pos, left_pos, right_pos):
                if new_pos in cave:
                    continue
                if new_pos.y == lowest_y:
                    falling_away = True
                    break
                if new_pos not in cave:
                    path.append(new_pos)
                    pos = new_pos
                    break
            else:
                can_fall = False
                cave[pos] = "o"
                path.pop()
        if falling_away:
            break
        sands += 1

    return sands


def calc2(cave: Dict[Coord, str]) -> int:
    sands = 0

    start = Coord(500, 0)
    path = [start]
    lowest_y = max([point.y for point in cave])
    floor = lowest_y + 2

    while True:
        pos = path[-1]
        can_fall = True
        while can_fall:
            down_pos = Coord(pos.x, pos.y + 1)
            left_pos = Coord(pos.x - 1, pos.y + 1)
            right_pos = Coord(pos.x + 1, pos.y + 1)
            for new_pos in (down_pos, left_pos, right_pos):
                if new_pos in cave or new_pos.y == floor:
                    continue
                if new_pos not in cave:
                    path.append(new_pos)
                    pos = new_pos
                    break
            else:
                can_fall = False
                cave[pos] = "o"
                path.pop()
        sands += 1
        if not path:
            break

    return sands


def print_cave(cave: Dict[Coord, str]):
    all_x = [point.x for point in cave]
    all_y = [point.y for point in cave]
    width = max(all_x) - min(all_x)
    height = max(all_y)
    start_x = min(all_x)
    for y in range(height + 1):
        for x in range(width + 1):
            coord = Coord(x + start_x, y)
            if coord in cave:
                print(cave[coord], end="")
            elif coord.x == 500 and coord.y == 0:
                print("+", end="")
            else:
                print(".", end="")
        # exit()
        print()


if __name__ == "__main__":
    data = read_data()
    print(calc1(data.copy()))
    print(calc2(data))
