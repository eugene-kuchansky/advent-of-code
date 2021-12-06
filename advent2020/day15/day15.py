import sys
from typing import Iterable, List, NamedTuple


def read_data(stream: Iterable[str]) -> List[int]:
    return [int(num) for line in stream for num in line.strip().split(",")]


def calc1(nums: List[int], last_turn: int):
    memo = {num: (i, 0) for i, num in enumerate(nums, start=1)}
    last_num = nums[-1]

    for i in range(len(nums) + 1, last_turn + 1):
        last_spoken, last_spoken_prev = memo[last_num]
        if last_spoken_prev == 0:
            # previously the last num was spoken for the first time
            last_num = 0
        else:
            last_num = last_spoken - last_spoken_prev

        if last_num not in memo:
            info = (i, 0)
        else:
            last_spoken, last_spoken_prev = memo[last_num]
            info = (i, last_spoken)
        memo[last_num] = info
    return last_num


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)
    res1 = calc1(initial_data, 2020)
    print(f"result 1: {res1}")
    res2 = calc1(initial_data, 30000000)
    print(f"result 2: {res2}")
