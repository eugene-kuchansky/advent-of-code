import sys
from typing import List, Iterable
from collections import defaultdict
import math


def read_data(stream: Iterable[str]) -> List[int]:
    return [int(line.strip()) for line in stream]


def calc1(adapters: List[int]) -> List[int]:
    # add (first) charging outlet
    adapters.append(0)

    adapters.sort()

    # add (last) device joltage adapter
    device_adapter = adapters[-1] + 3
    adapters.append(device_adapter)

    diffs = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]
    return diffs


# the idea is empiric
# we need to find all sequences with elements diff equals to 1
# the minimum length of such sequence is 2
# here is the example:
# adapters=1 3 4 5 8
# diffs = 3 1 1 3
# there are only 2 ways to arrange this peace [1 1]
# 1) adapters=1 3 4 5 8
# 2) adapters=1 3 5 8
#
# in case when 3 one-diffs in a row there are 4 (1+3) way to arrange adapters:
# adapters=1 3 4 5 6 9
# diffs = 3 1 1 1 3
# 1) adapters=1 3 4 5 6 9
# 2) adapters=1 3 5 6 9
# 3) adapters=1 3 4 6 9
# 4) adapters=1 3 6 9
#
# for 4 one-diffs in a row there are 7 (4+3) way to arrange adapters
# for 5 one-diffs in a row there are 10 (7+3) way to arrange adapters and so on
#
# combination of variants is multiplied
# so as if there are 2 subsequences with lengths 2 and 3 then the result is 2 * 4 = 12
def calc2(diffs: List[int]) -> int:
    cnt = defaultdict(int)
    subsequence = []
    for diff in diffs:
        if diff != 3:
            subsequence.append(diff)
        else:
            if len(subsequence) > 1:
                cnt[len(subsequence)] += 1
            subsequence = []
    return int(math.pow(7, cnt[4])) * int(math.pow(4, cnt[3])) * int(math.pow(2, cnt[2]))


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res_diffs = calc1(initial_data)
    print(f"result 1: {res_diffs.count(3) * res_diffs.count(1)}")

    res2 = calc2(res_diffs)
    print(f"result 2: {res2}")
