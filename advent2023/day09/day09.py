import sys
from typing import List
from dataclasses import dataclass


@dataclass
class Node:
    name: str
    left: str
    right: str


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> [List[List[str]]]:
    numbers = []
    for line in lines:
        numbers.append([int(_) for _ in line.split(" ")])

    return numbers


def calc_next(sequence):
    diffs = []
    diffs.append(sequence)
    prev_line = sequence
    for i in range(len(sequence) - 1):
        new_line = []
        for i, num in enumerate(prev_line[1:], 1):
            new_line.append(num - prev_line[i - 1])
        diffs.append(new_line)
        prev_line = new_line

    for i, diff in enumerate(reversed(diffs[1:])):
        last = diff[-1]
        diffs[-2 - i].append(diffs[-2 - i][-1] + last)
    return diffs[0][-1]


def calc1(numbers: List[List[int]]) -> int:
    result = 0

    for seq in numbers:
        result += calc_next(list(seq))

    return result


def calc2(numbers: List[List[int]]) -> int:
    result = 0

    for seq in numbers:
        result += calc_next(list(reversed(seq)))

    return result


if __name__ == "__main__":
    raw_data = read_data()
    numbers = parse(raw_data)
    print(calc1(numbers))
    print(calc2(numbers))
