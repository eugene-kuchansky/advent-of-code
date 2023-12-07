import sys
from typing import List, Tuple, NamedTuple
from math import sqrt, ceil
from functools import reduce
import operator


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Tuple[List[int], List[int]]:
    times = [int(num) for num in lines[0].split(": ")[1].split(" ") if num]
    distances = [int(num) for num in lines[1].split(": ")[1].split(" ") if num]

    return times, distances


def next_int(num: float) -> int:
    # get the first int next to num
    # 1.0 -> 2
    # 1.1 -> 2

    if round(num) == int(num):
        return int(num) + 1
    return ceil(num)


def prev_int(num: float) -> int:
    # get the first int before the num
    # 2.0 -> 1
    # 2.1 -> 2

    if num == int(num):
        return int(num) - 1
    return int(num)


def resolve_quadratic_inequality(a: int, b: int, c: int) -> Tuple[int, int]:
    # D = b**2 - 4 * a * c
    # x1 = (-b + sqrt(D)) / (2* a)
    # x2 = (-b - sqrt(D)) / (2* a)

    d_big = b**2 - 4 * a * c

    x1 = (-b + sqrt(d_big)) / (2 * a)
    x2 = (-b - sqrt(d_big)) / (2 * a)

    lowest, highest = next_int(x1), prev_int(x2)
    return lowest, highest


def calc1(times: List[int], distances: List[int]) -> int:
    # equation:
    # velocity * (total_time - wait_time) = distance
    # velocity = wait_time
    #
    # wt * (t - wt) = d
    # -wt^2 + t * wt - d = 0
    #
    # a = -1
    # b = t
    # c = -d

    result = 1
    for t, d in zip(times, distances):
        lowers, highest = resolve_quadratic_inequality(-1, t, -d)
        win_count = highest - lowers + 1
        result *= win_count

    return result


def calc2(times: List[int], distances: List[int]) -> int:
    t = int("".join(str(num) for num in times))
    d = int("".join(str(num) for num in distances))

    lowers, highest = resolve_quadratic_inequality(-1, t, -d)

    result = highest - lowers + 1

    return result


if __name__ == "__main__":
    raw_data = read_data()
    times, distances = parse(raw_data)
    print(calc1(times, distances))
    print(calc2(times, distances))
