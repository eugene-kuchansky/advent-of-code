import sys
from typing import List, NamedTuple, Iterable, Set


class GroupAnswers(NamedTuple):
    people_answers: List[Set[str]]

    @property
    def combined_answers(self) -> Set[str]:
        return set.union(*self.people_answers)

    @property
    def common_answers(self) -> Set[str]:
        return set.intersection(*self.people_answers)

    @staticmethod
    def from_lines(lines: List[str]) -> "GroupAnswers":
        people = [set(line) for line in lines]
        return GroupAnswers(people)


def read_data(stream: Iterable[str]) -> List[GroupAnswers]:
    data = []
    people_answers = []
    for line in stream:
        if line == "\n":
            group = GroupAnswers.from_lines(people_answers)
            data.append(group)
            people_answers = []
            continue
        people_answers.append(line.strip())

    if people_answers:
        group = GroupAnswers.from_lines(people_answers)
        data.append(group)

    return data


def calc1(data: List[GroupAnswers]) -> int:
    return sum(len(group.combined_answers) for group in data)


def calc2(data: List[GroupAnswers]) -> int:
    return sum(len(group.common_answers) for group in data)


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)
    res1 = calc1(initial_data)
    print(f"result 1: {res1}")
    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
