import re
import sys
from typing import List


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def calc1(calibrations: List[str]) -> int:
    result = 0

    for row in calibrations:
        # find all numeric chars
        value = "".join(char for char in row if char.isdigit())
        # take first and last and cast to integer
        if value:
            result += int(f"{value[0]}{value[-1]}")

    return result


def calc2(calibrations: List[str]) -> int:
    word_to_num = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    # map keys and values of word_to_num to regex pattern
    # "(?=(...))" means that this is overlapping lookahead assertion
    # string "sevenine" is matched as ["seven" "nine"]
    pattern = re.compile(
        "(?=(" + "|".join(map(re.escape, list(word_to_num.keys()) + list(word_to_num.values()))) + "))"
    )

    fixed_calibrations = []

    def replacement_function(matched_group):
        match = matched_group.group(1)
        return word_to_num.get(match, match)

    for row in calibrations:
        # this will replace string "sevenine" with "7seve9nine"
        fixed_row = re.sub(pattern, replacement_function, row)
        fixed_calibrations.append(fixed_row)

    return calc1(fixed_calibrations)


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
