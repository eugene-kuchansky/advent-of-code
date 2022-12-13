import sys
from typing import List, Tuple
import json

from itertools import zip_longest
import functools


def read_data() -> List[Tuple[List, List]]:
    raw_data = sys.stdin.read()
    pairs = []
    for pair in raw_data.split("\n\n"):
        pair1, pair2 = pair.split("\n")
        pairs.append((json.loads(pair1), json.loads(pair2)))
    return pairs


def compare_pair(pair1, pair2) -> int:
    if isinstance(pair1, int) and isinstance(pair2, int):
        if pair1 < pair2:
            return -1
        elif pair1 > pair2:
            return 1
        return 0

    if isinstance(pair1, list) and isinstance(pair2, int):
        return compare_pair(pair1, [pair2])

    if isinstance(pair1, int) and isinstance(pair2, list):
        return compare_pair([pair1], pair2)

    if pair1 is None and pair2 is None:
        return 0

    if pair1 is None and pair2 is not None:
        return -1

    if pair1 is not None and pair2 is None:
        return 1

    if isinstance(pair1, list) and isinstance(pair2, list):
        for value1, value2 in zip_longest(pair1, pair2):
            result = compare_pair(value1, value2)
            if result != 0:
                return result
        return 0
    raise ValueError(f"wut '{pair1}=' '{pair2}='")


def calc1(pairs: List[Tuple[List, List]]) -> int:
    result = 0
    for i, pair in enumerate(pairs):
        compare_pair_result = compare_pair(pair[0], pair[1])
        if compare_pair_result == -1:
            result += i + 1

    return result


def calc2(pairs: List[Tuple[List, List]]) -> int:
    divider_packet1 = [[2]]
    divider_packet2 = [[6]]

    packets = [divider_packet1, divider_packet2]
    for pair in pairs:
        packets.append(pair[0])
        packets.append(pair[1])

    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare_pair))

    result = 1
    for i, packet in enumerate(sorted_packets):
        if packet == divider_packet1:
            result = result * (i + 1)
        elif packet == divider_packet2:
            result = result * (i + 1)
    return result


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
