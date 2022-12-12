import sys
from typing import List, Dict, Optional, Callable, Tuple
from dataclasses import dataclass, field
from operator import mul, add


@dataclass
class Operation:
    expression: str
    divide_by: int = 1
    op: Callable = field(init=False)
    op_str: str = ""
    arg2: Optional[int] = None

    def __post_init__(self):
        _, calc_part = self.expression.split(" = ")
        if "+" in calc_part:
            op = "+"
            self.op = add
            self.op_str = "increases by"
        else:
            op = "*"
            self.op = mul
            self.op_str = "is multiplied"

        _, arg2 = calc_part.split(f" {op} ")
        if arg2 != "old":
            self.arg2 = int(arg2)

    def calc(self, value):
        old = value
        if self.arg2 is None:
            arg2 = old
        else:
            arg2 = self.arg2
        new_value = self.op(old, arg2)
        # print(f"    Worry level {self.op_str} by {arg2} to {new_value}")
        new_value = new_value // self.divide_by
        # print(f"    Monkey gets bored with item. Worry level is divided by {self.divide_by} to {new_value}.")
        return new_value


@dataclass
class Monkey:
    id: int
    items: List[int]
    operation: Operation
    divisible_by: int
    pass_to: Dict[bool, int]
    inspects_num: int = 0

    def inspect(self) -> List[Tuple[int, int]]:
        pass_to = []
        for item in self.items:
            self.inspects_num += 1
            monkey_id, new_item = self.inspect_item(item)
            pass_to.append((monkey_id, new_item))
        self.items = []
        return pass_to

    def inspect_item(self, item) -> Tuple[int, int]:
        # print(f"  Monkey inspects an item with a worry level of {item}.")
        new_item = self.operation.calc(item)
        is_divisible = new_item % self.divisible_by == 0
        # is_divisible_str = "divisible" if is_divisible else "not divisible"
        # print(f"    Current worry level is {is_divisible_str} by {self.divisible_by}.")

        monkey_id = self.pass_to[is_divisible]
        # print(f"    Item with worry level {new_item} is thrown to monkey {monkey_id}.")
        return (monkey_id, new_item)


def read_data() -> List[Monkey]:
    raw_data = sys.stdin.read()
    monkeys = []
    for monkey_id, monkey_data in enumerate(raw_data.split("\n\n")):
        _, starting_items_data, expression_data, divisible_data, if_true_data, if_false_data = monkey_data.split("\n")
        items_data = starting_items_data.split(": ")
        if len(items_data) > 1:
            starting_items = [int(item) for item in items_data[1].split(", ")]
        else:
            starting_items = []

        expression = expression_data.split(": ")[1]
        operation = Operation(expression, divide_by=3)
        divisible = int(divisible_data.split(" ")[-1])
        if_true_monkey = int(if_true_data.split(" ")[-1])
        if_false_monkey = int(if_false_data.split(" ")[-1])

        monkey = Monkey(
            id=monkey_id,
            items=starting_items,
            operation=operation,
            divisible_by=divisible,
            pass_to={True: if_true_monkey, False: if_false_monkey},
        )
        monkeys.append(monkey)

    return monkeys


def calc1(monkeys: List[Monkey]) -> int:
    for _ in range(20):
        for monkey in monkeys:
            # print(f"Monkey {monkey.id}")
            for new_monkey, item in monkey.inspect():
                monkeys[new_monkey].items.append(item)
    monkey_business = []
    for monkey in monkeys:
        # print(f"Monkey {monkey.id} inspected items {monkey.inspects_num} times.")
        monkey_business.append(monkey.inspects_num)
    monkey_business.sort(reverse=True)
    m1, m2, *_ = monkey_business
    return m1 * m2


def calc2(monkeys: List[Monkey]) -> int:
    gcd = 1
    for monkey in monkeys:
        gcd *= monkey.divisible_by

    for _ in range(10000):
        for monkey in monkeys:
            for new_monkey, item in monkey.inspect():
                item = item % gcd
                monkeys[new_monkey].items.append(item)
    monkey_business = []
    for monkey in monkeys:
        # print(f"Monkey {monkey.id} inspected items {monkey.inspects_num} times.")
        monkey_business.append(monkey.inspects_num)
    monkey_business.sort(reverse=True)
    m1, m2, *_ = monkey_business
    return m1 * m2


if __name__ == "__main__":
    data = read_data()
    data_copy = [
        Monkey(
            id=monkey.id,
            items=list(monkey.items),
            operation=Operation(monkey.operation.expression, divide_by=1),
            divisible_by=monkey.divisible_by,
            pass_to=monkey.pass_to,
        )
        for monkey in data
    ]
    print(calc1(data))
    print(calc2(data_copy))
