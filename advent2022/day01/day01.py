import sys
from typing import List


def read_data() -> List[int]:
    elves = []
    raw_data = sys.stdin.read()
    for elves_data in raw_data.split("\n\n"):
        calories = sum([int(calories) for calories in elves_data.split("\n")])
        elves.append(calories)
    return elves


def calc1(elves: List[int]) -> int:
    return max(elves)


def calc2(elves: List[int]) -> int:
    return sum(sorted(elves, reverse=True)[:3])


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
