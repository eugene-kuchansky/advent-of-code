import math
import sys
from functools import lru_cache


def read_data() -> list[int]:
    raw_data = sys.stdin.read().strip()
    stones = []

    for stone in raw_data.split(" "):
        stones.append(int(stone))

    return stones


@lru_cache(maxsize=None)
def get_next(stone: int, steps: int) -> int:
    stones = []
    if stone == 0:
        stones.append(1)
    else:
        num_digits = int(math.log10(abs(stone))) + 1
        if num_digits % 2 == 0:
            stone1 = stone // 10 ** (num_digits // 2)
            stone2 = stone % 10 ** (num_digits // 2)
            stones.append(stone1)
            stones.append(stone2)
        else:
            stones.append(stone * 2024)
    if steps == 1:
        return len(stones)
    else:
        return sum(get_next(s, steps - 1) for s in stones)


def calc1(stones: list[int]) -> int:
    result = 0

    for stone in stones:
        result += get_next(stone, 25)
    return result


def calc2(stones: list[int]) -> int:
    result = 0

    for stone in stones:
        result += get_next(stone, 75)
    return result


if __name__ == "__main__":
    stones = read_data()
    print(calc1(stones))
    print(calc2(stones))
