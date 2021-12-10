from typing import List
from statistics import median


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """16,1,2,0,4,2,7,1,2,14"""


def parse(raw: str) -> List[int]:
    return [int(position) for position in raw.split(",")]


def calc(positions: List[int]) -> int:
    min_val = min(positions)
    max_val = max(positions)
    min_moves = None
    for i in range(min_val, max_val + 1):
        moves = sum(abs(position - i) for position in positions)
        if min_moves is None or min_moves > moves:
            min_moves = moves
    if min_moves is None:
        raise ValueError("min_moves is not found")
    return min_moves


def calc_median(positions: List[int]) -> int:
    med = int(median(positions))
    min_moves = sum(abs(position - med) for position in positions)
    return min_moves


def sum_progression(n: int) -> int:
    return n * (n + 1) // 2


def calc2(positions: List[int]) -> int:
    min_val = min(positions)
    max_val = max(positions)
    min_moves = None
    for i in range(min_val, max_val + 1):
        moves = sum(sum_progression(abs(position - i)) for position in positions)
        if min_moves is None or min_moves > moves:
            min_moves = moves
    if min_moves is None:
        raise ValueError("min_moves is not found")
    return min_moves


assert calc(parse(RAW)) == 37
# assert calc2(parse(RAW)) == 168


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data)))
    print(calc_median(parse(raw_data)))
    # print(calc2(parse(raw_data)))
