import sys
from collections import namedtuple
from typing import NamedTuple
class Move(NamedTuple):
    num: int
    from_stack: int
    to_stack: int


def read_data():
    raw_data = sys.stdin.read()
    crates_data, moves_data = raw_data.split('\n\n')
    crates = crates_data.split('\n')
    stacks_num = int(crates[-1].strip()[-1])
    crates = list(reversed(crates[:-1]))
    # print(crates)
    stacks = [list() for _ in range(stacks_num)]
    for line in crates:
        for i in range(stacks_num):
            pos = 1 + i * 4
            if pos >= len(line):
                break
            if line[pos] == ' ':
                continue
            stacks[i].append(line[pos])
    # print(stacks)
    moves = []
    for move in moves_data.split('\n'):
        # move 1 from 2 to 1
        _, num, _, from_stack, _, to_stack = move.split(' ')
        moves.append(Move(int(num), int(from_stack) - 1, int(to_stack) - 1))
    # print(moves)
    return stacks, moves


def calc1(orig_stacks, moves):
    stacks = [list(stack) for stack in orig_stacks]
    for move in moves:
        for _ in range(move.num):
            val = stacks[move.from_stack].pop()
            stacks[move.to_stack].append(val)
    # print(stacks)
    top_crates = [stack[-1] for stack in stacks]
    return ''.join(top_crates)


def calc2(stacks, moves):
    for move in moves:
        crates = stacks[move.from_stack][-move.num:]
        stacks[move.from_stack] = stacks[move.from_stack][:-move.num]
        stacks[move.to_stack].extend(crates)
    top_crates = [stack[-1] for stack in stacks]
    return ''.join(top_crates)


if __name__ == "__main__":
    stacks, moves = read_data()

    print(calc1(stacks, moves))
    print(calc2(stacks, moves))
