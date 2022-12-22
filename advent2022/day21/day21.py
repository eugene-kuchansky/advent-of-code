import sys
from typing import Dict, Set, List, Optional
from dataclasses import dataclass, replace


@dataclass
class Monkey:
    name: str
    value: Optional[int] = None
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    op: Optional[str] = None

    def calc(self, monkeys: Dict[str, "Monkey"]) -> int:
        if self.value is not None:
            return self.value
        if monkeys[self.arg1].value is None:
            monkeys[self.arg1].calc(monkeys)
        arg1 = monkeys[self.arg1].value
        if monkeys[self.arg2].value is None:
            monkeys[self.arg2].calc(monkeys)
        arg2 = monkeys[self.arg2].value

        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.value = operations[self.op](arg1, arg2)
        return self.value


def read_data() -> Dict[str, Monkey]:
    raw_data = sys.stdin.read()
    monkeys: Dict[str, Monkey] = {}
    for line in raw_data.split("\n"):
        name, rest = line.split(": ")
        if " " in rest:
            arg1, op, arg2 = rest.split(" ")
            monkey = Monkey(name=name, arg1=arg1, arg2=arg2, op=op)
        else:
            monkey = Monkey(name=name, value=int(rest))
        monkeys[name] = monkey

    return monkeys


def calc1(orig_monkeys: Dict[str, Monkey]) -> int:
    monkeys = {name: replace(monkey) for name, monkey in orig_monkeys.items()}
    return int(monkeys["root"].calc(monkeys))


def calc2(monkeys: Dict[str, Monkey]) -> int:
    monkeys["humn"].value = 1j
    arg1 = monkeys[monkeys["root"].arg1].calc(monkeys)
    arg2 = monkeys[monkeys["root"].arg2].calc(monkeys)
    if isinstance(arg2, complex):
        arg1, arg2 = arg2, arg1
    return int((arg2 - arg1.real) / arg1.imag)


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
