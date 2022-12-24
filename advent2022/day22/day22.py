import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
import re


@dataclass(frozen=True)
class Point:
    row: int = 0
    col: int = 0

    def __add__(self, point: "Point") -> "Point":
        return Point(self.row + point.row, col=self.col + point.col)

    def __sub__(self, point: "Point") -> "Point":
        return Point(self.row - point.row, col=self.col - point.col)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point):
            raise ValueError("cannot compare")
        return self.col == __o.col and self.row == __o.row


@dataclass
class Move:
    steps: int = 0
    turn: str = ""


WALL = "#"
SPACE = "."
VOID = " "

RIGHT = ">"
DOWN = "v"
LEFT = "<"
UP = "^"

DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
OPPOSITE_DIRECTIONS = {
    RIGHT: LEFT,
    DOWN: UP,
    LEFT: RIGHT,
    UP: DOWN,
}
VECTOR = {
    RIGHT: Point(row=0, col=1),
    DOWN: Point(row=1, col=0),
    LEFT: Point(row=0, col=-1),
    UP: Point(row=-1, col=0),
}


@dataclass
class Direction:
    dir: str = DIRECTIONS[0]

    def rotate(self, turn: str):
        ind = DIRECTIONS.index(self.dir)
        if turn == "R":
            self.dir = DIRECTIONS[(ind + 1) % 4]
        elif turn == "L":
            self.dir = DIRECTIONS[ind - 1]
        else:
            raise ValueError("wrong turn!")


@dataclass
class Samurai:
    # A samurai has no goal, only path
    board: Dict[Point, str]
    path: List[Move]
    dir: Direction
    coord: Point

    def go(self):
        for move in self.path:
            if move.turn:
                self.dir.rotate(move.turn)
                continue
            vector = VECTOR[self.dir.dir]

            for _ in range(move.steps):
                new_coord = self.adjust_coord(self.coord + vector)
                if self.board.get(new_coord, "") == WALL:
                    break
                self.coord = new_coord

    def adjust_coord(self, coord: Point) -> Point:
        if coord in self.board:
            return coord
        new_col = coord.col
        new_row = coord.row
        rows = (tile.row for tile in self.board if tile.col == coord.col)
        cols = (tile.col for tile in self.board if tile.row == coord.row)
        if self.dir.dir == UP:
            new_row = max(rows)
        elif self.dir.dir == DOWN:
            new_row = min(rows)
        elif self.dir.dir == RIGHT:
            new_col = min(cols)
        elif self.dir.dir == LEFT:
            new_col = max(cols)
        else:
            raise ValueError("wut")

        return Point(row=new_row, col=new_col)


@dataclass
class Samurai2:
    # A samurai has no goal, only path
    board: Dict[Point, str]
    path: List[Move]
    dir: Direction
    coord: Point
    face: int = 1
    cube_size: int = 0
    faces_coords: Dict[int, Point] = field(default_factory=dict)
    faces_directions: Dict[int, Dict[str, int]] = field(default_factory=dict)

    def __post_init__(self):
        self.faces_directions = {
            1: {RIGHT: 2, DOWN: 3, LEFT: 4, UP: 5},
            2: {RIGHT: 6, DOWN: 3, LEFT: 1, UP: 5},
            3: {RIGHT: 2, DOWN: 6, LEFT: 4, UP: 1},
            4: {RIGHT: 1, DOWN: 3, LEFT: 6, UP: 5},
            5: {RIGHT: 2, DOWN: 1, LEFT: 4, UP: 6},
            6: {RIGHT: 4, DOWN: 3, LEFT: 2, UP: 5},
        }

    def go(self):
        self.get_cube_faces()
        for move in self.path:
            if move.turn:
                self.dir.rotate(move.turn)
                continue
            vector = VECTOR[self.dir.dir]

            for _ in range(move.steps):
                vector = VECTOR[self.dir.dir]
                new_coord, new_dir, new_face = self.adjust_coord(self.coord + vector)
                if self.board.get(new_coord, "") == WALL:
                    break
                self.coord = new_coord
                self.dir = new_dir
                self.face = new_face

    def adjust_coord(self, coord: Point) -> Tuple[Point, Direction, int]:
        top_left = self.faces_coords[self.face]

        if (top_left.row + self.cube_size) > coord.row >= top_left.row and (
            top_left.col + self.cube_size
        ) > coord.col >= top_left.col:
            return coord, self.dir, self.face

        new_face = self.faces_directions[self.face][self.dir.dir]

        new_top_left = self.faces_coords[new_face]

        back_dir = {face: dir for dir, face in self.faces_directions[new_face].items()}[self.face]
        new_dir = Direction(OPPOSITE_DIRECTIONS[back_dir])

        d_col = new_top_left.col - top_left.col
        d_row = new_top_left.row - top_left.row

        if new_dir.dir == RIGHT:
            d_col -= self.cube_size
        elif new_dir.dir == LEFT:
            d_col += self.cube_size
        elif new_dir.dir == UP:
            d_row += self.cube_size
        elif new_dir.dir == DOWN:
            d_row -= self.cube_size

        new_coord = coord + Point(row=d_row, col=d_col)
        top_left = top_left + Point(row=d_row, col=d_col)

        old_dir_ind = DIRECTIONS.index(self.dir.dir)
        new_dir_ind = DIRECTIONS.index(new_dir.dir)

        rotate_num = (new_dir_ind - old_dir_ind) % 4
        for _ in range(rotate_num):
            d_col = new_coord.col - top_left.col
            d_row = new_coord.row - top_left.row
            new_coord = Point(row=top_left.row + d_col, col=top_left.col + self.cube_size - d_row - 1)

        return new_coord, new_dir, new_face

    def calc_cube_size(self) -> None:
        width = max(coord.col for coord in board) + 1
        height = max(coord.row for coord in board) + 1

        if width // 3 == height // 4:
            self.cube_size = width // 3
        elif width // 4 == height // 3:
            self.cube_size = width // 4
        elif width // 2 == height // 4:
            self.cube_size = width // 2
        elif width // 4 == height // 2:
            self.cube_size = width // 4
        else:
            raise ValueError("incorrect size")

    def get_cube_faces(self) -> None:
        self.calc_cube_size()
        col = min(coord.col for coord, tile in board.items() if coord.row == 0 and tile == SPACE)
        self.faces_coords[1] = Point(row=0, col=col)

        q = []
        q.append((self.face, 0, ""))
        while q:
            face, from_face, from_dir = q.pop(0)
            face_coord = self.faces_coords[face]

            right = Point(row=0, col=self.cube_size) + face_coord
            left = Point(row=0, col=-self.cube_size) + face_coord
            top = Point(row=-self.cube_size, col=0) + face_coord
            bottom = Point(row=self.cube_size, col=0) + face_coord

            while from_face and self.faces_directions[face][OPPOSITE_DIRECTIONS[from_dir]] != from_face:
                curr_dirs = list(self.faces_directions[face].keys())
                curr_faces = list(self.faces_directions[face].values())
                curr_faces.append(curr_faces.pop(0))
                self.faces_directions[face] = dict(zip(curr_dirs, curr_faces))

            for point, dir in zip((right, bottom, left, top), DIRECTIONS):
                if point in board:
                    new_face = self.faces_directions[face][dir]
                    if new_face not in self.faces_coords:
                        self.faces_coords[new_face] = point
                        q.append((new_face, face, dir))


def read_data() -> Tuple[Dict[Point, str], List[Move]]:
    raw_data = sys.stdin.read()
    board_data, path_data = raw_data.split("\n\n")
    board: Dict[Point, str] = {}
    path: List[Move] = []

    for r, row in enumerate(board_data.split("\n")):
        for c, tile in enumerate(row):
            if tile == VOID:
                continue
            board[Point(row=r, col=c)] = tile

    for value in re.split(r"(R|L)", path_data):
        try:
            steps = int(value)
            path.append(Move(steps=steps))
        except ValueError:
            path.append(Move(turn=value))

    return board, path


def print_board(board, s: Point):
    max_col = max(tile.col for tile in board)
    max_row = max(tile.row for tile in board)

    for r in range(max_row + 1):
        for c in range(max_col + 1):
            if c == s.col and r == s.row:
                print("S", end="")
            else:
                print(board.get(Point(row=r, col=c), " "), end="")
        print()
    print()


def calc1(board: Dict[Point, str], path: List[Move]) -> int:
    col = min(coord.col for coord, tile in board.items() if coord.row == 0 and tile == SPACE)
    samurai = Samurai(board, path, Direction(), Point(col=col))
    samurai.go()
    return (samurai.coord.row + 1) * 1000 + (samurai.coord.col + 1) * 4 + DIRECTIONS.index(samurai.dir.dir)


def calc2(board: Dict[Point, str], path: List[Move]) -> int:
    col = min(coord.col for coord, tile in board.items() if coord.row == 0 and tile == SPACE)
    samurai_3d = Samurai2(board, path, Direction(), Point(col=col))
    samurai_3d.go()
    return (samurai_3d.coord.row + 1) * 1000 + (samurai_3d.coord.col + 1) * 4 + DIRECTIONS.index(samurai_3d.dir.dir)


if __name__ == "__main__":
    board, path = read_data()
    print(calc1(board, path))
    print(calc2(board, path))
