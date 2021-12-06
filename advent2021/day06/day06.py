from typing import List
from dataclasses import dataclass
from functools import lru_cache


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """3,4,3,1,2"""


def parse(raw: str) -> List[int]:
    return [int(timer) for timer in raw.split(",")]


@lru_cache(1000)
def calc_fresh_fish(days):
    if days < 7:
        return 0
    created_new_fishes = days // 7
    total = created_new_fishes
    for i in range(created_new_fishes):
        days -= 7
        total += calc_fresh_fish(days - 2)
    return total


def calc_fish(days, timer):
    total = 1
    if timer != 6:
        days -= timer - 6
    total += calc_fresh_fish(days)
    return total


def calc(fishes: List[int], days: int) -> int:
    total = 0
    for timer in fishes:
        total += calc_fish(days, timer)

    return total


assert calc(parse(RAW), days=18) == 26
assert calc(parse(RAW), days=80) == 5934


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data), days=80))
    print(calc(parse(raw_data), days=256))
