from string import ascii_uppercase
from collections import deque, defaultdict

TELEPORT_SYMBOL = ascii_uppercase
WAY = "."

MOVES = ((0, 1), (0, -1), (1, 0), (-1, 0))


def read_data(file_name):
    with open(file_name) as f:
        raw_data = f.read()
    lines = raw_data.split("\n")
    ways = set()
    all_teleports = {}
    max_lines = len(lines)
    len_line = len(lines[0])

    outer_teleports = set()
    inner_teleports = set()

    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value == WAY:
                # part of maze path
                ways.add((x, y))
            elif value in TELEPORT_SYMBOL:
                # teleport
                if y + 3 <= max_lines and lines[y + 1][x] in TELEPORT_SYMBOL and lines[y + 2][x] == WAY:
                    # from bottom (AB)
                    #
                    #     A
                    #     B
                    # ####.####
                    name = f"{value}{lines[y + 1][x]}"
                    pos = (x, y + 2)
                    all_teleports[pos] = name
                    if y == 0:
                        outer_teleports.add(pos)
                    else:
                        inner_teleports.add(pos)
                elif 1 < y + 1 < max_lines and lines[y + 1][x] in TELEPORT_SYMBOL and lines[y - 1][x] == WAY:
                    # from top (XY)
                    #
                    # ####.####
                    #     X
                    #     Y
                    name = f"{value}{lines[y + 1][x]}"
                    pos = (x, y - 1)
                    all_teleports[pos] = name
                    if y == max_lines - 2:
                        outer_teleports.add(pos)
                    else:
                        inner_teleports.add(pos)
                elif x + 3 < len_line and line[x + 1] in TELEPORT_SYMBOL and line[x + 2] == WAY:
                    # from right (MN)
                    #
                    #    #
                    #  MN.
                    #    #
                    name = f"{value}{line[x + 1]}"
                    pos = (x + 2, y)
                    all_teleports[(x + 2, y)] = name
                    if x == 0:
                        outer_teleports.add(pos)
                    else:
                        inner_teleports.add(pos)
                elif 1 < x + 1 < len_line and line[x + 1] in TELEPORT_SYMBOL and line[x - 1] == WAY:
                    # from left (WZ)
                    #
                    #  #
                    #  .WZ
                    #  #
                    name = f"{value}{line[x + 1]}"
                    all_teleports[(x - 1, y)] = name
                    pos = (x - 1, y)
                    if x == len_line - 2:
                        outer_teleports.add(pos)
                    else:
                        inner_teleports.add(pos)
    teleports = {}
    start_point = (0, 0)
    end_point = (0, 0)

    for coord, name in all_teleports.items():
        # if coord in inner_teleports:
        #     print(f"{name} {coord} - inner")
        # elif coord in outer_teleports:
        #     print(f"{name} {coord} - outer")
        # else:
        #     print(f"{name} {coord} - wut")

        if name == "AA":
            start_point = coord
        elif name == "ZZ":
            end_point = coord
        else:
            if coord not in teleports:
                for coord2, name2 in all_teleports.items():
                    if name == name2 and coord != coord2:
                        teleports[coord] = coord2
                        teleports[coord2] = coord
                        break

    return ways, start_point, end_point, teleports, outer_teleports, inner_teleports


def shortest_path(ways, start_point, end_point, teleports):
    queue = deque()
    steps = {start_point: 0}

    queue.append((start_point, 0))

    while queue:
        pos, step_num = queue.popleft()
        steps[pos] = step_num

        if pos in teleports:
            pos = teleports[pos]
            step_num += 1
            steps[pos] = step_num

        if pos == end_point:
            return step_num

        x, y = pos
        for (dx, dy) in MOVES:
            new_pos = (x + dx, y + dy)
            if new_pos not in ways or new_pos in steps:
                continue
            queue.append((new_pos, step_num + 1))
    return steps[end_point]


def shortest_path2(ways, start_point, end_point, teleports, outer_teleports, inner_teleports):
    queue = deque()
    level = 0
    steps = defaultdict(dict)
    steps[level][start_point] = 0

    queue.append((start_point, 0, level))

    while queue:
        pos, step_num, level = queue.popleft()
        # print(f"pos {pos}, step_num {step_num}, level {level}")
        steps[level][pos] = step_num

        if pos in teleports and not (level == 0 and pos in outer_teleports):
            pos = teleports[pos]
            step_num += 1
            if pos in inner_teleports:
                level += 1
            else:
                level -= 1
            steps[level][pos] = step_num

        if pos == end_point and level == 0:
            return step_num

        (x, y) = pos
        for (dx, dy) in MOVES:
            new_pos = (x + dx, y + dy)
            if new_pos not in ways or new_pos in steps[level]:
                continue
            queue.append((new_pos, step_num + 1, level))


def part1():
    ways, start_point, end_point, teleports, _, _ = read_data("input_data/20_demo.txt")
    res = shortest_path(ways, start_point, end_point, teleports)
    print(res)


def part2():
    ways, start_point, end_point, teleports, outer_teleports, inner_teleports = read_data("input_data/20.txt")
    res = shortest_path2(ways, start_point, end_point, teleports, outer_teleports, inner_teleports)
    print(res)


if __name__ == "__main__":
    part1()
    part2()

