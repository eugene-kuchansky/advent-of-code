import sys
from typing import Dict, List, Tuple, NamedTuple
from dataclasses import dataclass, field
from collections import defaultdict

BLIZZARDS = (">", "<", "^", "v")


class Point(NamedTuple):
    row: int = 0
    col: int = 0


MOVE_AROUND = (Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1), Point(0, 0))

Board = Dict[Point, List[str]]


def read_data() -> Tuple[Board, Point, Point]:
    raw_data = sys.stdin.read()
    rows = raw_data.split("\n")
    board: Board = defaultdict(list)

    for r, row in enumerate(rows):
        for c, tile in enumerate(row):
            if tile in BLIZZARDS:
                board[Point(r, c)].append(tile)

    enter_col = next(col for col, tile in enumerate(rows[0]) if tile == ".")
    exit_col = next(col for col, tile in enumerate(rows[-1]) if tile == ".")
    start_point = Point(row=0, col=enter_col)
    exit_point = Point(row=len(rows) - 1, col=exit_col)

    return board, start_point, exit_point


@dataclass
class Expotition:
    board: Board
    start_point: Point
    exit_point: Point
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0
    walkers: Dict[Point, str] = field(default_factory=dict)
    board_repeated_step: int = 0
    minutes: int = 0

    def __post_init__(self):
        self.left = 1
        self.right = exit_point.col
        self.top = 1
        self.bottom = exit_point.row - 1
        self.walkers[self.start_point] = "E"

    def swap(self) -> None:
        self.start_point, self.exit_point = self.exit_point, self.start_point
        self.walkers: Dict[Point, str] = {self.start_point: "E"}
        self.board_repeated_step += self.minutes + 1

    def go(self):
        while True:
            board = self.move_blizzards()
            walkers = self.move_walkers(board)
            self.board = board
            self.walkers = walkers
            self.minutes += 1

            if self.exit_point in self.walkers:
                break
        return self.minutes

    def move_walkers(self, board: Board) -> Dict[Point, str]:
        walkers: Dict[Point, str] = {}
        walkers[self.start_point] = "E"

        for point in self.walkers:
            for move in MOVE_AROUND:
                new_point = Point(point[0] + move[0], point[1] + move[1])
                if new_point in walkers or new_point == self.start_point or board[new_point]:
                    continue
                if (
                    new_point.col < self.left
                    or new_point.col > self.right
                    or new_point.row < self.top
                    or new_point.row > self.bottom
                ) and new_point != self.exit_point:
                    continue
                walkers[new_point] = "E"

        return walkers

    def move_blizzards(self) -> Board:
        new_board = defaultdict(list)
        for point, blizzards in self.board.items():
            for blizz in blizzards:
                new_board[self.get_next_coord(point, blizz)].append(blizz)
        return new_board

    def get_next_coord(self, point: Point, blizz: str) -> Point:
        col = point.col
        row = point.row
        if blizz == ">":
            col = col + 1 if col < self.right else self.left
        elif blizz == "<":
            col = col - 1 if col > self.left else self.right
        elif blizz == "v":
            row = row + 1 if row < self.bottom else self.top
        elif blizz == "^":
            row = row - 1 if row > self.top else self.bottom
        else:
            raise ValueError(f"wut {blizz}")
        return Point(row, col)

    def print_board(self):
        for col in range(self.right + 2):
            p = Point(row=self.top - 1, col=col)
            if p not in (self.start_point, self.exit_point):
                print("#", end="")
            elif p in self.walkers:
                print("E", end="")
            else:
                print(".", end="")
        print()
        for r in range(1, self.bottom + 1):
            print("#", end="")
            for c in range(1, self.right + 1):
                p = Point(row=r, col=c)
                if len(self.board[p]) == 0:
                    if p in self.walkers:
                        print(self.walkers[p], end="")
                    else:
                        print(".", end="")
                elif len(self.board[p]) == 1:
                    if p in self.walkers:
                        raise ValueError("wut")
                    print(self.board[p][0], end="")
                else:
                    if p in self.walkers:
                        raise ValueError("wut")
                    print(len(self.board[p]), end="")
            print("#")

        for col in range(self.right + 2):
            p = Point(row=self.bottom + 1, col=col)
            if p not in (self.start_point, self.exit_point):
                print("#", end="")
            elif p in self.walkers:
                print("E", end="")
            else:
                print(".", end="")
        print()
        print()


def calc1(board: Board, start_point: Point, exit_point: Point) -> int:
    ex = Expotition(board, start_point, exit_point)
    return ex.go()


def calc2(board: Board, start_point: Point, exit_point: Point) -> int:
    ex = Expotition(board, start_point, exit_point)
    ex.go()
    ex.swap()
    ex.go()
    ex.swap()
    return ex.go()


if __name__ == "__main__":
    board, start_point, exit_point = read_data()
    # print(calc1(board, start_point, exit_point))
    print(calc2(board, start_point, exit_point))
