import sys
from typing import List, NamedTuple, Dict, Tuple, Callable
from operator import gt, lt
from copy import deepcopy


class XMAS(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_str(cls, s) -> "XMAS":
        pairs = s.strip("{}").split(",")
        d = {}
        for pair in pairs:
            name, value = pair.split("=")
            d[name] = int(value)
        return cls(**d)


class Condition(NamedTuple):
    attr_name: str
    op: Callable
    compare_value: int
    result: str

    def __call__(self, xmas: XMAS) -> str:
        if self.op(getattr(xmas, self.attr_name), self.compare_value):
            return self.result
        return ""

    @classmethod
    def from_str(cls, s) -> "Condition":
        signs = {
            ">": gt,
            "<": lt,
        }
        operation, result = s.split(":")

        attr_name = operation[0]
        op = signs[operation[1]]
        compare_value = int(operation[2:])

        return cls(attr_name=attr_name, op=op, compare_value=compare_value, result=result)


class Rule(NamedTuple):
    name: str
    conditions: List[Condition]
    else_value: str

    def apply(self, xmas: XMAS) -> str:
        for condition in self.conditions:
            res = condition(xmas)
            if res:
                return res
        return self.else_value

    @classmethod
    def from_str(cls, s) -> "Rule":
        name, conditions_str = s.split("{")
        conditions_def = conditions_str.strip("{}").split(",")
        else_value = conditions_def[-1]
        conditions_def = conditions_def[:-1]

        conditions = [Condition.from_str(op) for op in conditions_def]
        return Rule(name=name, conditions=conditions, else_value=else_value)


def read_data() -> List[str]:
    raw_data = sys.stdin.read()

    res = [line for line in raw_data.split("\n")]
    if not res[-1]:
        return res[:-1]


def parse(lines: List[str]) -> Tuple[List[XMAS], Dict[str, Rule]]:
    rules = {}
    xmases = []
    ind = lines.index("")
    for line in lines[:ind]:
        rule = Rule.from_str(line)
        rules[rule.name] = rule

    for line in lines[ind + 1 :]:
        xmas = XMAS.from_str(line)
        xmases.append(xmas)
    return xmases, rules


def calc1(xmases: List[XMAS], rules: Dict[str, Rule]) -> int:
    result = 0
    combos = merge_rules(rules)
    for xmas in xmases:
        for combo in combos:
            if apply(xmas, combo):
                result += xmas.x + xmas.m + xmas.a + xmas.s
                break
    # for xmas in xmases:
    #     rule_name = "in"
    #     rule = rules[rule_name]
    #     while (res := rule.apply(xmas)) not in {"R", "A"}:
    #         rule = rules[res]
    #     if res == "A":
    #         result += xmas.x + xmas.m + xmas.a + xmas.s

    return result


def merge_rules(rules: Dict[str, Rule]):
    name = "in"
    initial_combo = {letter: [0, 4001] for letter in "xmas"}
    combos = check_rule(rules, name, initial_combo)
    return combos


def add_opposite_condition(condition: Condition, combo: Dict[str, List[int]]) -> Dict[str, List[int]]:
    reverse_compare = {
        gt: lt,
        lt: gt,
    }

    compare_value = condition.compare_value
    if condition.op == gt:
        compare_value += 1
    else:
        compare_value -= 1
    opposite_condition = Condition(
        attr_name=condition.attr_name,
        op=reverse_compare[condition.op],
        compare_value=compare_value,
        result=condition.result,
    )
    return add_condition(opposite_condition, combo)


def add_condition(condition: Condition, combo: Dict[str, List[int]]) -> Dict[str, List[int]]:
    new_combo = deepcopy(combo)
    attr = condition.attr_name
    value = condition.compare_value
    if condition.op == gt:
        new_combo[attr][0] = max(new_combo[attr][0], value)
    else:
        new_combo[attr][1] = min(new_combo[attr][1], value)

    return new_combo


def check_rule(rules: Dict[str, Rule], name: str, combo: Dict[str, List[int]]) -> List[Dict[str, List[int]]]:
    if name == "A":
        return [combo]

    if name == "R":
        return []

    rule = rules[name]
    good_combos = []

    current_combo = deepcopy(combo)

    for condition in rule.conditions:
        new_combo = add_condition(condition, current_combo)
        res = check_rule(rules, name=condition.result, combo=new_combo)
        good_combos.extend(res)
        current_combo = add_opposite_condition(condition, current_combo)

    res = check_rule(rules, name=rule.else_value, combo=current_combo)
    good_combos.extend(res)

    return good_combos


def apply(xmas, combo):
    for letter in "xmas":
        if not (combo[letter][1] > getattr(xmas, letter) > combo[letter][0]):
            return False
    return True


def calc2(rules: Dict[str, Rule]) -> int:
    result = 0
    combos = merge_rules(rules)

    for combo in combos:
        prod = 1
        for letter in "xmas":
            prod *= combo[letter][1] - combo[letter][0] - 1
        result += prod

    return result


if __name__ == "__main__":
    raw_data = read_data()
    xmases, rules = parse(raw_data)
    print(calc1(xmases, rules))
    print(calc2(rules))
