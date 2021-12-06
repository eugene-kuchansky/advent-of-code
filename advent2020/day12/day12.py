import sys
from typing import Iterable, Tuple, List, NamedTuple, Dict


class Coord(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    x: int
    y: int


DIRECTIONS = [
    Direction(0, 1),  # North
    Direction(1, 0),  # East
    Direction(0, -1),  # South
    Direction(-1, 0),  # West
]

ROTATE = {
    1: lambda coord: Coord(coord.y, -coord.x),  # 90
    2: lambda coord: Coord(-coord.x, -coord.y),  # 180
    3: lambda coord: Coord(-coord.y, coord.x),  # 270
}


class Action:
    def execute(self, position: Coord, direction: Direction) -> Tuple[Coord, Direction]:
        pass

    def execute2(self, position: Coord, waypoint: Coord) -> Tuple[Coord, Coord]:
        pass


class Move(NamedTuple, Action):
    direction: Direction
    value: int

    @staticmethod
    def parse(direction: str, value: int) -> "Move":
        to_direction: Dict[str, Direction] = {
            "N": DIRECTIONS[0],
            "E": DIRECTIONS[1],
            "S": DIRECTIONS[2],
            "W": DIRECTIONS[3],
        }
        return Move(to_direction[direction], value)

    def execute(self, position: Coord, direction: Direction) -> Tuple[Coord, Direction]:
        x = position.x + self.value * self.direction.x
        y = position.y + self.value * self.direction.y
        return Coord(x, y), direction

    def execute2(self, position: Coord, waypoint: Coord) -> Tuple[Coord, Coord]:
        x = waypoint.x + self.value * self.direction.x
        y = waypoint.y + self.value * self.direction.y
        return position, Coord(x, y)


class Rotate(NamedTuple, Action):
    degree: int

    @staticmethod
    def parse(direction: str, value: int):
        if direction == "L":
            value = -value
        return Rotate(int(value / 90))

    def execute(self, position: Coord, direction: Direction) -> Tuple[Coord, Direction]:
        direction_ind = DIRECTIONS.index(direction)
        new_direction_ind = (direction_ind + self.degree) % 4
        return position, DIRECTIONS[new_direction_ind]

    def execute2(self, position: Coord, waypoint: Coord) -> Tuple[Coord, Coord]:
        degree = self.degree % 4
        return position, ROTATE[degree](waypoint)


class Forward(NamedTuple, Action):
    value: int

    def execute(self, position: Coord, direction: Direction) -> Tuple[Coord, Direction]:
        x = position.x + self.value * direction.x
        y = position.y + self.value * direction.y
        return Coord(x, y), direction

    def execute2(self, position: Coord, waypoint: Coord) -> Tuple[Coord, Coord]:
        x = position.x + self.value * waypoint.x
        y = position.y + self.value * waypoint.y
        return Coord(x, y), waypoint


def get_action(item: str) -> Action:
    action, value = item[0], item[1:]
    if action in ("R", "L"):
        return Rotate.parse(action, int(value))
    elif action == "F":
        return Forward(int(value))
    return Move.parse(action, int(value))


def read_data(stream: Iterable[str]) -> List[Action]:
    return [get_action(line.strip()) for line in stream]


def calc1(actions: List[Action]) -> int:
    position = Coord(0, 0)
    direction = DIRECTIONS[1]

    for action in actions:
        position, direction = action.execute(position, direction)

    return abs(position.x) + abs(position.y)


def calc2(actions: List[Action]) -> int:
    position = Coord(0, 0)
    waypoint = Coord(10, 1)

    for action in actions:
        position, waypoint = action.execute2(position, waypoint)

    return abs(position.x) + abs(position.y)


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
