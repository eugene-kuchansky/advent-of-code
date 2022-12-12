import sys
from typing import Iterable, Set, Tuple, List, Optional
from functools import lru_cache

EMPTY = "L"
OCCUPIED = "#"

Seat = Tuple[int, int]


class Layout:
    MAX_OCCUPIED = 4
    DIRECTIONS = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )

    def __init__(self, seats: Set[Seat], width: int, height: int):
        self.seats = seats
        self.area = {seat: EMPTY for seat in seats}
        self.width = width
        self.height = height

    @lru_cache(maxsize=100000000)
    def get_neighbours(self, seat: Seat) -> List[Seat]:
        neighbours = []
        for (x, y) in self.DIRECTIONS:
            neighbour = self.check_neighbour(seat, x, y)
            if neighbour:
                neighbours.append(neighbour)

        return neighbours

    def check_neighbour(self, seat: Seat, dx, dy) -> Optional[Seat]:
        x, y = seat
        other_seat = (x + dx, y + dy)
        if other_seat in self.seats:
            return other_seat
        return None

    def get_seat_status(self, seat: Seat) -> str:
        occupied_num = 0
        current_state = self.area[seat]
        for neighbour in self.get_neighbours(seat):
            if self.area[neighbour] == OCCUPIED:
                occupied_num += 1

        if current_state == OCCUPIED and occupied_num >= self.MAX_OCCUPIED:
            return EMPTY

        if current_state == EMPTY and occupied_num == 0:
            return OCCUPIED

        return current_state

    def calc(self):
        while True:
            area = {seat: self.get_seat_status(seat) for seat in self.seats}
            if area == self.area:
                break
            self.area = area

        return sum(status == OCCUPIED for status in self.area.values())


class Layout2(Layout):
    MAX_OCCUPIED = 5

    def check_neighbour(self, seat: Seat, dx, dy) -> Optional[Seat]:
        x, y = seat
        x += dx
        y += dy

        while 0 <= x <= self.width and 0 <= y <= self.height:
            other_seat = (x, y)
            if other_seat in self.seats:
                return other_seat
            x += dx
            y += dy

        return None


def read_data(stream: Iterable[str]) -> Tuple[Set[Seat], int, int]:
    seats = set()
    width = 0
    height = 0

    # i know, kinda ugly
    for y, line in enumerate(stream):
        for x, place in enumerate(line):
            if place == EMPTY:
                seats.add((x, y))
            width = x
        height = y
    return seats, width, height


def calc1(seats: Set[Seat], width: int, height: int):
    layout = Layout(seats, width, height)
    return layout.calc()


def calc2(seats: Set[Seat], width: int, height: int) -> int:
    layout = Layout2(seats, width, height)
    return layout.calc()


if __name__ == "__main__":
    initial_data, area_width, area_height = read_data(sys.stdin)

    res1 = calc1(initial_data, area_width, area_height)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data, area_width, area_height)
    print(f"result 2: {res2}")
