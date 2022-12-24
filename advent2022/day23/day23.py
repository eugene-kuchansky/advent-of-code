import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Point:
    row: int = 0
    col: int = 0

    def __add__(self, point: "Point") -> "Point":
        return Point(self.row + point.row, col=self.col + point.col)

    def __sub__(self, point: "Point") -> "Point":
        return Point(self.row - point.row, col=self.col - point.col)

    # def __eq__(self, __o: object) -> bool:
    #     if not isinstance(__o, Point):
    #         raise ValueError("cannot compare")
    #     return self.col == __o.col and self.row == __o.row


def read_data() -> Dict[Point, str]:
    raw_data = sys.stdin.read()
    rows = raw_data.split("\n")
    board: Dict[Point, str] = {}

    for r, row in enumerate(rows):
        for c, tile in enumerate(row):
            if tile == "#":
                board[Point(r, c)] = "#"

    return board


def print_board(board: Dict[Point, str]):
    max_col = max(tile.col for tile in board)
    max_row = max(tile.row for tile in board)

    min_col = min(tile.col for tile in board)
    min_row = min(tile.row for tile in board)

    for r in range(min_row - 1, max_row + 2):
        for c in range(min_col - 1, max_col + 2):
            print(board.get(Point(row=r, col=c), "."), end="")
        print()
    print()


def count_empty(board: Dict[Point, str]) -> int:
    max_col = max(tile.col for tile in board)
    max_row = max(tile.row for tile in board)

    min_col = min(tile.col for tile in board)
    min_row = min(tile.row for tile in board)
    result = 0
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if Point(row=r, col=c) not in board:
                result += 1
    return result


AROUND = (
    Point(-1, 0),
    Point(-1, 1),
    Point(-1, -1),
    Point(0, 1),
    Point(0, -1),
    Point(1, 1),
    Point(1, 0),
    Point(1, -1),
)

CHECK_NORTH = (
    Point(-1, -1),
    Point(-1, 0),
    Point(-1, 1),
)

CHECK_SOUTH = (
    Point(1, 1),
    Point(1, 0),
    Point(1, -1),
)

CHECK_EAST = (
    Point(-1, 1),
    Point(0, 1),
    Point(1, 1),
)

CHECK_WEST = (
    Point(1, -1),
    Point(0, -1),
    Point(-1, -1),
)

CHECK_DIRECTIONS = {"^": CHECK_NORTH, "v": CHECK_SOUTH, "<": CHECK_WEST, ">": CHECK_EAST}

GO_DIRECTIONS = {"^": Point(-1, 0), "v": Point(1, 0), "<": Point(0, -1), ">": Point(0, 1)}


def get_new_board(board: Dict[Point, str], directions: List[str]) -> Tuple[Dict[Point, str], bool]:
    step_board: Dict[Point, List[Point]] = defaultdict(list)
    has_moves = False
    for coord in board:
        for check_around in AROUND:
            if (coord + check_around) in board:
                break
        else:
            if step_board[coord]:
                raise ValueError("wut")
            step_board[coord] = [coord]
            continue

        can_go = False
        for direction in directions:
            if can_go:
                break

            for check in CHECK_DIRECTIONS[direction]:
                new_coord = coord + check
                if new_coord in board:
                    break
            else:
                step_board[coord + GO_DIRECTIONS[direction]].append(coord)
                has_moves = True
                can_go = True
                break
        else:
            step_board[coord].append(coord)
            continue

    new_board: Dict[Point, str] = {}
    for coord, points in step_board.items():
        if len(points) == 1:
            new_board[coord] = "#"
        else:
            for point in points:
                new_board[point] = "#"
    return new_board, has_moves


def calc1(board: Dict[Point, str]) -> int:
    rounds = 10
    directions = ["^", "v", "<", ">"]
    for _ in range(rounds):
        board, _ = get_new_board(board, directions)
        first = directions.pop(0)
        directions.append(first)
    return count_empty(board)


def calc2(board: Dict[Point, str]) -> int:
    rounds = 1
    directions = ["^", "v", "<", ">"]
    while True:
        board, has_moves = get_new_board(board, directions)
        if not has_moves:
            break
        first = directions.pop(0)
        directions.append(first)
        rounds += 1

    return rounds


if __name__ == "__main__":
    board = read_data()
    print(calc1(board))
    print(calc2(board))
