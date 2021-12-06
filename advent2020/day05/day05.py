import sys
from typing import List, NamedTuple, Iterable
import operator


def decode_binary(value: str, one: str, zero: str) -> int:
    return int(value.replace(one, "1").replace(zero, "0"), 2)


class Seat(NamedTuple):
    row: int
    column: int
    id: int

    @staticmethod
    def from_string(value: str) -> "Seat":
        row = decode_binary(value[:7], one="B", zero="F")
        column = decode_binary(value[7:], one="R", zero="L")
        id_ = row * 8 + column
        return Seat(row=row, column=column, id=id_)


def read_data(stream: Iterable[str]) -> List[Seat]:
    return [Seat.from_string(line.strip()) for line in stream]


def calc1(data: List[Seat]) -> int:
    return max(seat.id for seat in data)


def calc2(data: List[Seat]) -> int:
    prev_seat_id = None
    for seat in sorted(data, key=operator.attrgetter("id")):
        if prev_seat_id is None:
            prev_seat_id = seat.id
            continue
        if seat.id > prev_seat_id + 1:
            return prev_seat_id + 1
        prev_seat_id = seat.id

    return -1


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)
    res1 = calc1(initial_data)
    print(f"result 1: {res1}")
    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
