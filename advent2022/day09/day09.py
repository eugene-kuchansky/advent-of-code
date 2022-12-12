import sys
from typing import List, Set, NamedTuple
from math import copysign


class Move(NamedTuple):
    direction: str
    steps: int


class Position(NamedTuple):
    x: int
    y: int


def read_data():
    moves = []
    for line in sys.stdin.readlines():
        direction, steps = line.strip().split(" ")
        moves.append(Move(direction, int(steps)))
    return moves


def move_tail(head: Position, tail: Position) -> Position:
    new_x = tail.x
    new_y = tail.y
    dx = head.x - tail.x
    dy = head.y - tail.y
    if (abs(dx) + abs(dy)) in (3, 4):
        # move diagonally
        new_x += int(copysign(1, dx))
        new_y += int(copysign(1, dy))
    elif abs(dx) == 2:
        # move horizontally
        new_x += int(copysign(1, dx))
    elif abs(dy) == 2:
        # move vertically
        new_y += int(copysign(1, dy))

    return Position(new_x, new_y)


def move_head(head: Position, direction: str) -> Position:
    directions = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    dx, dy = directions[direction]
    return Position(head.x + dx, head.y + dy)


def calc1(moves: List[Move]) -> int:
    head = Position(0, 0)
    tail = Position(0, 0)
    positions: Set[Position] = set()
    positions.add(tail)
    for move in moves:
        for _ in range(move.steps):
            head = move_head(head, move.direction)
            tail = move_tail(head, tail)
            positions.add(tail)

    return len(positions)


def calc2(moves: List[Move]) -> int:
    head = Position(0, 0)
    tails = [Position(0, 0) for _ in range(9)]
    positions: Set[Position] = set()
    positions.add(tails[-1])

    for move in moves:
        for _ in range(move.steps):
            head = move_head(head, move.direction)
            head_x = head
            for i, tail in enumerate(tails):
                tail = move_tail(head_x, tail)
                tails[i] = tail
                head_x = tail
            positions.add(tails[-1])

    return len(positions)


def print_field(head, tails):
    field = [["." for _ in range(27)] for _ in range(22)]
    shift_y = 6
    shift_x = 11
    field[head.y + shift_y][head.x + shift_x] = "H"
    for i, tail in enumerate(tails):
        if field[tail.y + shift_y][tail.x + shift_x] == ".":
            field[tail.y + shift_y][tail.x + shift_x] = str(i + 1)

    if field[0 + shift_y][0 + shift_x] == ".":
        field[0 + shift_y][0 + shift_x] = "s"

    for row in reversed(field):
        print("".join(row))

    print("\n\n")


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
