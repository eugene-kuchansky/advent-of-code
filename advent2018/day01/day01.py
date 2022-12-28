import sys
from typing import List
from itertools import cycle


def read_data() -> List[int]:
    raw_data = sys.stdin.read()
    return [int(_) for _ in raw_data.split("\n")]


def calc1(data: List[int]) -> int:
    return sum(data)


def calc2(data: List[int]) -> int:
    seen = set()
    freq = 0
    for num in cycle(data):
        freq += num
        if freq in seen:
            return freq
        seen.add(freq)


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
