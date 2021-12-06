import sys
from typing import List, Iterable, Tuple, Dict
import operator
from collections import defaultdict


OPERATORS = {
    "+": operator.add,
    "*": operator.mul,
}


def parse_expr(expression: str) -> List[str]:
    expr = []
    for item in expression.split(" "):
        expr.extend(list(item))
    return expr


def read_data(stream: Iterable[str]) -> List[List[str]]:
    return [parse_expr(line.strip()) for line in stream]


def apply_operator(a: int, b: int, op: str) -> int:
    return OPERATORS[op](a, b)


def perform_operation(operators: List[str], values: List[int]) -> Tuple[List[str], List[int]]:
    value = apply_operator(values.pop(), values.pop(), op=operators.pop())
    values.append(value)
    return operators, values


def calculate(expression: List[str], precedence: Dict[str, int]) -> int:
    values = []
    operators = []
    for i, item in enumerate(expression):
        if item == "(":
            operators.append(item)
        elif item.isnumeric():
            values.append(int(item))
        elif item in "+*":
            while operators and precedence[operators[-1]] >= precedence[item]:
                operators, values = perform_operation(operators, values)
            operators.append(item)
        elif item == ")":
            while operators and operators[-1] != "(":
                operators, values = perform_operation(operators, values)
            operators.pop()

    while operators:
        operators, values = perform_operation(operators, values)

    return values.pop()


def calc1(expressions: List[List[str]]) -> int:
    precedence = defaultdict(int, {"+": 1, "*": 1})
    return sum(calculate(expression, precedence) for expression in expressions)


def calc2(expressions: List[List[str]]) -> int:
    precedence = defaultdict(int, {"+": 2, "*": 1})
    return sum(calculate(expression, precedence) for expression in expressions)


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
