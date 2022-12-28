import sys
from typing import List
from collections import Counter
from time import time


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return list(raw_data.split("\n"))


def calc1(data: List[str]) -> int:
    two_letters = 0
    three_letters = 0
    for word in data:
        letters_counts = set(Counter(word).values())
        two_letters += int(2 in letters_counts)
        three_letters += int(3 in letters_counts)
    return two_letters * three_letters


def calc2(data: List[int]) -> str:
    for i, word in enumerate(data[:-1]):
        for other_word in data[i + 1 :]:
            diff = 0
            for l1, l2 in zip(word, other_word):
                if l1 != l2:
                    diff += 1
                    if diff > 1:
                        break
            else:
                common_letters = "".join(
                    [l1 for l1, l2 in zip(word, other_word) if l1 == l2]
                )
                return common_letters
    return ""


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
