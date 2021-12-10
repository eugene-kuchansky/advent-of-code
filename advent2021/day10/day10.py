from typing import List
from dataclasses import dataclass, field
from enum import Enum


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


class Result(Enum):
    CORRECT = 1
    INCOMPLETE = 2
    CORRUPTED = 3


RAW = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

CORRUPTED_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

INCOMPLETE_SCORE = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
OPENING = set(PAIRS.keys())


@dataclass
class Subsystem:
    chunk: str
    incorrect_char: str = ""
    incomplete: List[str] = field(default_factory=list)

    def check(self) -> Result:
        stack: List[str] = []
        for char in self.chunk:
            if char in OPENING:
                stack.append(char)
            elif PAIRS[stack[-1]] != char:
                self.incorrect_char = char
                return Result.CORRUPTED
            else:
                stack.pop()

        if stack:
            self.incomplete = stack
            return Result.INCOMPLETE

        return Result.CORRECT

    def calc_incomplete_score(self):
        score = 0
        for char in self.incomplete[::-1]:
            score = score * 5 + INCOMPLETE_SCORE[char]
        return score


def parse(raw: str) -> List[Subsystem]:
    return [Subsystem(line) for line in raw.split("\n")]


def calc(subsystems: List[Subsystem]) -> int:
    score = 0
    for subsystem in subsystems:
        if subsystem.check() == Result.CORRUPTED:
            score += CORRUPTED_SCORE[subsystem.incorrect_char]
    return score


def calc2(subsystems: List[Subsystem]) -> int:
    scores = []
    for subsystem in subsystems:
        if subsystem.check() == Result.INCOMPLETE:
            print(subsystem.incomplete)
            scores.append(subsystem.calc_incomplete_score())
    sorted_scores = sorted(scores)
    middle_score = sorted_scores[(len(sorted_scores) - 1) // 2]
    return middle_score


assert calc(parse(RAW)) == 26397
assert calc2(parse(RAW)) == 288957


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data)))
    print(calc2(parse(raw_data)))
