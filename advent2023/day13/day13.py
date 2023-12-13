import sys
from typing import List


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n")]


def parse(lines: List[str]) -> List[List[str]]:
    patterns = []
    pattern = []
    for line in lines:
        if not line:
            patterns.append(pattern)
            pattern = []
            continue
        pattern.append(line)
    return patterns


def diff(a, b) -> int:
    # return 0 if equal. else 1
    return int(a != b)


def diff_in_one_bit_or_eq(a, b) -> int:
    # return zero if equal
    # return 1 if diff in 1 bit
    # else return 100
    if a == b:
        return 0
    xor_result = a ^ b
    if xor_result and not (xor_result & (xor_result - 1)):
        return 1
    return 100


def find_mirror_horizontal(pattern: List[str], op, valid_result: int) -> int:
    numbers = to_numbers(pattern)
    return find_reflection(numbers, op=op, valid_result=valid_result)


def find_mirror_vertical(pattern: List[str], op, valid_result: int) -> int:
    horizontal_pattern = turn_right(pattern)
    numbers = to_numbers(horizontal_pattern)
    return find_reflection(numbers, op=op, valid_result=valid_result)


def to_numbers(pattern: List[str]) -> List[int]:
    # just convert line into value to compare binary
    numbers = []
    for line in pattern:
        n = int(line.replace("#", "1").replace(".", "0"), 2)
        numbers.append(n)
    return numbers


def find_reflection(numbers: List[int], op, valid_result) -> int:
    # check every line if there is a reflection point
    for i, _ in enumerate(numbers[:-1]):
        if sum(op(a, b) for a, b in zip(reversed(numbers[: i + 1]), numbers[i + 1 :])) == valid_result:
            return i + 1


def turn_right(lst: List[str]) -> List[str]:
    # transpose matrix - rotate to 90 degree to the right
    return ["".join(reversed("".join(row))) for row in zip(*lst)]


def calc1(patterns: List[List[str]]) -> int:
    result = 0
    for pattern in patterns:
        # check if lines are equal. if equal then 0, else 1
        # sum the rows, expected value is zero
        r1 = find_mirror_horizontal(pattern, op=diff, valid_result=0)
        r2 = find_mirror_vertical(pattern, op=diff, valid_result=0)

        # just in case try both variants
        if not (r1 or r2):
            raise Exception("cannot find reflection")
        if r1 and r2:
            raise Exception("found two reflection")
        result += r2 or r1 * 100

    return result


def calc2(patterns: List[List[str]]) -> int:
    result = 0
    for pattern in patterns:
        # check if lines are equal.
        # if equal then 0
        # else if diff is 1 bit then 1
        # else then 100
        # sum the rows, expected value is one
        r1 = find_mirror_horizontal(pattern, op=diff_in_one_bit_or_eq, valid_result=1)
        r2 = find_mirror_vertical(pattern, op=diff_in_one_bit_or_eq, valid_result=1)

        # just in case try both variants
        if not (r1 or r2):
            raise Exception("cannot find reflection")
        if r1 and r2:
            raise Exception("found two reflection")
        result += r2 or r1 * 100

    return result


if __name__ == "__main__":
    raw_data = read_data()
    patterns = parse(raw_data)
    print(calc1(patterns))
    print(calc2(patterns))
