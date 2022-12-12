import sys
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Section:
    left: int
    right: int

    def __len__(self):
        return self.right - self.left


def read_data():
    assignments = []
    for line in sys.stdin:
        line = line.rstrip()
        pairs = [pair.split("-") for pair in line.split(",")]
        values = [int(i) for pair in pairs for i in pair]
        assignments.append((Section(values[0], values[1]), Section(values[2], values[3])))
    return assignments


def calc1(data: List[Tuple[Section, Section]]):
    fully_contained = 0
    for pair1, pair2 in data:
        # pair1 should is bigger or equal to pair2
        # otherwise swap
        if len(pair2) > len(pair1):
            pair1, pair2 = pair2, pair1
        if pair1.left <= pair2.left and pair1.right >= pair2.right:
            fully_contained += 1
    return fully_contained


def calc2(data: List[Tuple[Section, Section]]):
    overlapped = 0
    for pair1, pair2 in data:
        # pair1 should be on left of pair2
        # otherwise swap
        if pair2.left < pair1.left:
            pair1, pair2 = pair2, pair1
        if pair1.right >= pair2.left:
            overlapped += 1
    return overlapped


if __name__ == "__main__":
    raw_data = read_data()

    print(calc1(raw_data))
    print(calc2(raw_data))
