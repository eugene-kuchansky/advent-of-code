import sys
from typing import List, Dict, NamedTuple, Set


class Coord(NamedTuple):
    x: int
    y: int


UP: Coord = (0, -1)
DOWN: Coord = (0, 1)
LEFT: Coord = (-1, 0)
RIGHT: Coord = (1, 0)


PIPE_DIR: Dict[str, Coord] = {
    "|": [UP, DOWN],
    "-": [LEFT, RIGHT],
    "L": [UP, RIGHT],
    "J": [UP, LEFT],
    "7": [DOWN, LEFT],
    "F": [DOWN, RIGHT],
    "S": [UP, DOWN, LEFT, RIGHT],
    ".": [],
}


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Dict[Coord, str]:
    maze = {}
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            maze[Coord(x, y)] = symbol

    return maze


def get_moves(pipe: str, coord: Coord) -> List[Coord]:
    moves = []
    for move in PIPE_DIR[pipe]:
        moves.append(Coord(move[0] + coord[0], move[1] + coord[1]))
    return moves


def can_move_here(pipe: str, coord: Coord, from_coord: Coord):
    for move in PIPE_DIR[pipe]:
        if Coord(move[0] + coord[0], move[1] + coord[1]) == from_coord:
            return True
    return False


def get_start_coord(maze: Dict[Coord, str]) -> Coord:
    for coord, pipe in maze.items():
        if pipe == "S":
            return coord
    else:
        raise Exception("Start not found")


# def get_pipe_old(maze: Dict[Coord, str]) -> Dict[Coord, int]:
#     # good old dfs. it's overkill for plain looped pipe
#     start_coord = get_start_coord(maze)

#     visited = {start_coord: 0}
#     q = deque()
#     q.append(start_coord)

#     while q:
#         coord = q.popleft()
#         pipe = maze[coord]
#         move_coords = get_moves(pipe, coord)
#         for new_coord in move_coords:
#             if new_coord in visited:
#                 continue

#             if new_coord not in maze:
#                 continue

#             if not can_move_here(maze[new_coord], new_coord, coord):
#                 continue

#             visited[new_coord] = visited[coord] + 1
#             q.append(new_coord)

#     return visited


def get_pipes(maze: Dict[Coord, str]) -> Set[Coord]:
    # start from the start and visit all pipes connected elements once
    coord = get_start_coord(maze)
    visited = {coord}

    while True:
        pipe = maze[coord]

        move_coords = get_moves(pipe, coord)
        for new_coord in move_coords:
            if new_coord in visited:
                continue

            if new_coord not in maze:
                continue

            if not can_move_here(maze[new_coord], new_coord, coord):
                continue

            visited.add(new_coord)
            coord = new_coord
            break
        else:
            # stop if nowhere to move
            break

    return visited


def calc1(maze: Dict[Coord, str]) -> int:
    # get all pipes elements
    pipes = get_pipes(maze)
    # the farthest point is the half of the whole pipes length
    result = len(pipes) // 2
    return result


def calc2(maze: Dict[Coord, str]) -> int:
    result = 0

    start_coord = get_start_coord(maze)

    pipes = get_pipes(maze)
    max_x, max_y = max(maze)

    # let's use point-to-polygon algorithm
    # 1. take a point and draw a line to any direction (to the right in this case)
    # calc how many times it crosses the pipe
    # if the number is even - it is outside
    # if is odd - inside

    for coord in maze:
        # check all non-pipes elements. call them dots
        if coord in pipes:
            continue

        if coord[0] == 0 or coord[0] == max_x or coord[1] == 0 or coord[1] == max_y:
            continue

        line = []

        # take all elements from the right of the dot
        # but only if start coord is not in the same line and is to the right.
        # if it is in the same line, we take a line to the left of the current point
        # because we don't know the pipe element in the start point
        # we could determine it but i'm a bit lazy
        if start_coord[1] == coord[1] and start_coord[0] > coord[0]:
            # line to the left
            start_line = 0
            end_line = coord[0]
        else:
            # line to the right
            start_line = coord[0] + 1
            end_line = max_x + 1

        for x in range(start_line, end_line):
            # check all the pipes elements in the line and keep only whose with vertical parts
            next_coord = Coord(x, coord[1])
            next_right = maze[next_coord]

            if next_coord not in pipes or next_right == "-":
                continue

            line.append(next_right)

        # the tricky part
        # 1. if the line to the right contains loop like ".╔═══╗" or ".╚═══╝" the dot is outside the loop
        # 2. but if it crosses like ".╔═══╝" or ".╚═══╗" the dot is inside the loop
        # so keep odd/even number of crossed pipes so we just
        # remove cases 1.
        # leave only single element in case 2.
        clean_line = "".join(line)
        clean_line = clean_line.replace("F7", "")
        clean_line = clean_line.replace("LJ", "")
        clean_line = clean_line.replace("FJ", "|")
        clean_line = clean_line.replace("L7", "|")

        if len(clean_line) % 2 == 1:
            # hey, the dot is inside
            result += 1

    return result


if __name__ == "__main__":
    raw_data = read_data()
    maze = parse(raw_data)
    print(calc1(maze))
    print(calc2(maze))
