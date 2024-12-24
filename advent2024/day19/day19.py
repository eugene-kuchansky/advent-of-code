import sys
from functools import lru_cache


def read_data() -> tuple[list[str], list[str]]:
    raw_data = sys.stdin.read()
    patterns, towels = raw_data.strip().split("\n\n")
    patterns = patterns.split(", ")
    towels = towels.split("\n")
    return patterns, towels


@lru_cache(maxsize=None)
def validate_pattern(towel: str, patterns: tuple[str, ...]) -> int:
    result = 0
    if not towel:
        return 1
    for pattern in patterns:
        if towel.startswith(pattern):
            result += validate_pattern(towel.removeprefix(pattern), patterns)
    return result


def calc1(patterns: list[str], towels: list[str]) -> int:
    result = 0
    for towel in towels:
        if validate_pattern(towel, tuple(patterns)):
            result += 1
    return result


def calc2(patterns: list[str], towels: list[str]) -> str:
    result = 0

    for towel in towels:
        result += validate_pattern(towel, tuple(patterns))

    return result


if __name__ == "__main__":
    patterns, towels = read_data()
    print(calc1(patterns, towels))
    print(calc2(patterns, towels))
