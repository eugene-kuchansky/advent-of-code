from typing import List
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


@dataclass
class Params:
    id: int
    div_z: int
    add_x: int
    add_y: int


def parse(raw: str) -> List[Params]:
    lines = raw.splitlines()
    params = []

    for i in range(len(lines) // 18):
        sub_program = lines[i * 18 : (i + 1) * 18]
        div_z = int(sub_program[4].split(" ")[-1])
        add_x = int(sub_program[5].split(" ")[-1])
        add_y = int(sub_program[15].split(" ")[-1])
        params.append(Params(i, div_z, add_x, add_y))
    return params


"""
well, I've had to look at megasolution posts to get the idea
program is divided into 14 parts by 18 commands which are same except lines 4, 5 and 15
4 - div z 1/div z 26
5 - add x VAL1
15 - add y VAL2
programs starts with z= 0 and ends with it.
when 4 is "div z 1" subprogram is added some value to z register
when 4 is "div z 26" subprogram is allows to set to 0 last added value
there are exactly 7 subprograms of both types

simplified version of code looks like:
SOME_OPERATIONS * (1 if (1 if ((x1 + VAL1) + VAL2) == x2 else 0) == 0 else 0))
where x1 is value added to subprogram with "div z 1" and x2 to subprogram with "div z 26"
to set whole expression to zero we have to solve an equation: x1 + VAL1 + VAL2 == x2

since eliminating subprogram is always goes second we have to maximize x1 value
after that we put it to appropriate place of submarine fourteen-digit model number
hint: number of subprogram is the number of digit in model number
"""


def calc(params: List[Params], range_from, range_to, range_step) -> int:
    stack = []
    num = [1 for _ in range(14)]

    for param in params:
        if param.div_z == 1:
            stack.append(param)
        else:
            pair_param = stack.pop()
            for i in range(range_from, range_to, range_step):
                b = i + pair_param.add_y + param.add_x
                if 10 > b > 0:
                    num[pair_param.id] = i
                    num[param.id] = b
                    break
    return int("".join(str(_) for _ in num))


if __name__ == "__main__":
    raw = read_data()
    print(calc(parse(raw), 9, 0, -1))
    print(calc(parse(raw), 1, 10, 1))
