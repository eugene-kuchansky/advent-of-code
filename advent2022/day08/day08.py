import sys
from typing import List, Tuple
from functools import reduce
from operator import mul


def read_data():
    return [[int(tree) for tree in line.strip()] for line in sys.stdin.readlines()]


def calc1(trees: List[List[int]]) -> int:
    visibility = [[False for _ in range(len(trees[0]))] for _ in range(len(trees))]

    for row_num, row in enumerate(trees):
        # look right
        next_greater_or_equal = next_greater_or_equal_element(row)
        for col_num, next_greater_pos in enumerate(next_greater_or_equal):
            if next_greater_pos == -1:
                visibility[row_num][col_num] = True

        # look left
        next_greater_or_equal = next_greater_or_equal_element(row[::-1])
        for col_num, next_greater_pos in enumerate(next_greater_or_equal[::-1]):
            if next_greater_pos == -1:
                visibility[row_num][col_num] = True

    for col_num in range(len(trees[0])):
        column = [row[col_num] for row in trees]
        # look down
        next_greater_or_equal = next_greater_or_equal_element(column)
        for row_num, next_greater_pos in enumerate(next_greater_or_equal):
            if next_greater_pos == -1:
                visibility[row_num][col_num] = True

        # look up
        next_greater_or_equal = next_greater_or_equal_element(column[::-1])
        for row_num, next_greater_pos in enumerate(next_greater_or_equal[::-1]):
            if next_greater_pos == -1:
                visibility[row_num][col_num] = True

    visible_num = sum([sum(int(v) for v in row) for row in visibility])
    return visible_num


def next_greater_or_equal_element(lst: List[int]) -> List[int]:
    stack: List[Tuple[int, int]] = []
    result = [-1] * len(lst)

    for pos, value in enumerate(lst):
        if not stack:
            stack.append((pos, value))
            continue

        while stack:
            last_pos, last_value = stack[-1]
            if last_value > value:
                break
            stack.pop()
            result[last_pos] = pos

        stack.append((pos, value))

    return result


def calc2(trees: List[List[int]]) -> int:
    visibility = [[[0, 0, 0, 0] for _ in range(len(trees[0]))] for _ in range(len(trees))]

    for row_num, row in enumerate(trees):
        # look right
        next_greater_or_equal = next_greater_or_equal_element(row)
        for col_num, next_greater_pos in enumerate(next_greater_or_equal):
            if next_greater_pos == -1:
                next_greater_pos = len(row) - 1
            visibility[row_num][col_num][0] = next_greater_pos - col_num
        # look left
        next_greater_or_equal = next_greater_or_equal_element(row[::-1])
        next_greater_or_equal = [v if v != -1 else len(row) - 1 for v in next_greater_or_equal]
        dists_to_higher = [next_greater_pos - col_num for col_num, next_greater_pos in enumerate(next_greater_or_equal)]
        for col_num, dist in enumerate(dists_to_higher[::-1]):
            visibility[row_num][col_num][1] = dist

    for col_num in range(len(trees[0])):
        column = [row[col_num] for row in trees]
        # look down
        next_greater_or_equal = next_greater_or_equal_element(column)
        for row_num, next_greater_pos in enumerate(next_greater_or_equal):
            if next_greater_pos == -1:
                next_greater_pos = len(row) - 1
            visibility[row_num][col_num][2] = next_greater_pos - row_num

        # look up
        next_greater_or_equal = next_greater_or_equal_element(column[::-1])
        next_greater_or_equal = [v if v != -1 else len(row) - 1 for v in next_greater_or_equal]
        dists_to_higher = [next_greater_pos - row_num for row_num, next_greater_pos in enumerate(next_greater_or_equal)]

        for row_num, dist in enumerate(dists_to_higher[::-1]):
            visibility[row_num][col_num][3] = dist

    visible = max([reduce(mul, v, 1) for row in visibility for v in row])

    return visible


if __name__ == "__main__":
    trees = read_data()
    print(calc1(trees))
    print(calc2(trees))
