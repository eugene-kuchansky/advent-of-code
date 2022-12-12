import sys
from typing import List, NamedTuple


class Command(NamedTuple):
    name: str
    arg: int = 0


def read_data():
    commands = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if line == "noop":
            command = Command(line)
        else:
            name, value = line.split(" ")
            command = Command(name, int(value))

        commands.append(command)
    return commands


def get_signal(cycle, register) -> int:
    if cycle == 20 or (cycle - 20) % 40 == 0:
        return cycle * register
    return 0


def calc1(commands: List[Command]) -> int:
    register = 1
    cycle = 1
    signal = 0
    for command in commands:
        signal += get_signal(cycle, register)
        cycle += 1
        if command.name == "addx":
            signal += get_signal(cycle, register)
            cycle += 1
            register += command.arg

    return signal


def process_row(rows, cycle, register):
    row_num = (cycle - 1) // 40
    pos_num = (cycle - 1) % 40

    sprite_left = register - 1
    sprite_right = register + 1
    if sprite_left <= pos_num <= sprite_right:
        sprite = "#"
    else:
        sprite = "."
    rows[row_num][pos_num] = sprite
    return rows


def calc2(commands: List[Command]) -> str:
    register = 1
    cycle = 1
    rows = [["." for _ in range(40)] for _ in range(6)]

    for command in commands:
        rows = process_row(rows, cycle, register)
        cycle += 1
        if command.name == "addx":
            rows = process_row(rows, cycle, register)
            cycle += 1
            register += command.arg
    return "\n".join(["".join(row) for row in rows])


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
