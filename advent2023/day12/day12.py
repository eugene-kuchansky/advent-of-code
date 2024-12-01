import sys
from typing import List, Tuple


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Tuple[List[str], List[Tuple[int]]]:
    springs = []
    damaged_groups = []
    for line in lines:
        s, c = line.split(" ")
        springs.append(s)
        damaged_groups.append(tuple([int(_) for _ in c.split(",")]))
    return springs, damaged_groups


def sanitize_spring(spring: List[str]) -> List[str]:
    # remove extra spaces
    return ".".join([s for s in spring.strip(".").split(".") if s])


# @cache
def calc_arrangements(springs: str, damaged_groups: List[int]) -> int:
    # split into groups of springs separated by working spring "."
    springs_parts = springs.split(".")
    print()
    print("springs_parts", springs_parts)
    print("damaged_groups", damaged_groups)
    if len(springs_parts) == 1:
        return calc_part(springs, damaged_groups)

    first_part = springs_parts[0]
    other_parts = ".".join(springs_parts[1:])

    result = 0
    # try from zero to all damaged_groups to combine with first part of springs with the rest
    for i in range(len(damaged_groups) + 1):
        result += calc_arrangements(
            first_part,
            damaged_groups[:i],
        ) * calc_arrangements(
            other_parts,
            damaged_groups[i:],
        )
    return result


# @cache
def calc_part(springs: str, damaged_groups: Tuple[int]) -> int:
    print("  process", springs, damaged_groups)

    blocks_num = springs.count("#")

    if len(springs) < (sum(damaged_groups) + len(damaged_groups) - 1):
        print("  too small space for damage group", 0)
        return 0

    if blocks_num > sum(damaged_groups):
        print("  too small damaged groups", 0)
        return 0

    if "#" not in springs and len(damaged_groups) == 0:
        print("  no blocks, empty damaged_group", 1)
        return 1

    if "?" not in springs and len(damaged_groups) == 1 and sum(damaged_groups) == len(springs):
        print("  blocks equals to damaged_group", 1)
        return 1

    for i, symbol in enumerate(springs):
        if symbol == "?":
            part1 = calc_arrangements(springs[:i] + "#" + springs[i + 1 :], damaged_groups)
            part2 = calc_arrangements(springs[:i] + "." + springs[i + 1 :], damaged_groups)
            print("  part1 + part2", part1 + part2)
            return part1 + part2
    return 0


def calc1(all_springs: List[str], all_damaged_groups: List[Tuple[int]]) -> int:
    result = 0
    for springs, damaged_groups in zip(all_springs, all_damaged_groups):
        print(springs)
        print(damaged_groups)
        print("--------")
        springs = sanitize_spring(springs)
        r = calc_arrangements(springs, damaged_groups)
        # print("result", r)
        result += r
        exit()
        # print()

    return result


def calc2(springs: List[List[str]], conditions: List[List[int]]) -> int:
    result = 0
    for springs, damaged_groups in zip(all_springs, all_damaged_groups):
        springs5 = ((springs + "?") * 5)[:-1]
        damaged_groups5 = tuple(damaged_groups * 5)
        springs5 = sanitize_spring(springs5)
        result += calc_arrangements(springs5, damaged_groups5)

    return result


if __name__ == "__main__":
    raw_data = read_data()
    all_springs, all_damaged_groups = parse(raw_data)
    print(calc1(all_springs, all_damaged_groups))
    print(calc2(all_springs, all_damaged_groups))
