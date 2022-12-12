import sys
from typing import Iterable, Set, Tuple, NamedTuple, List, Dict
from itertools import product, chain


# initial class for rules which contains only links to other rules, no patterns
class RuleSchema(NamedTuple):
    id: int
    rule1: List[int]
    rule2: List[int]

    @staticmethod
    def parse(line: str) -> "RuleSchema":
        id_, value = line.split(": ")
        schemas = value.split(" | ")
        rule1 = [int(rule_id) for rule_id in schemas[0].split(" ")]
        rule2 = []
        if len(schemas) == 2:
            rule2 = [int(rule_id) for rule_id in schemas[1].split(" ")]

        return RuleSchema(int(id_), rule1=rule1, rule2=rule2)


# rule with all patterns
class Rule(NamedTuple):
    id: int
    patterns: List[str]

    @staticmethod
    def parse(line: str) -> "Rule":
        id_, value = line.split(": ")
        return Rule(int(id_), patterns=[value.strip('"')])


def read_data(stream: Iterable[str]) -> Tuple[Dict[int, Rule], Dict[int, RuleSchema], List[str]]:
    rules: Dict[int, Rule] = {}
    rules_schemas: Dict[int, RuleSchema] = {}

    for line in stream:
        line = line.strip()
        if not line:
            break
        if '"' in line:
            rule = Rule.parse(line)
            rules[rule.id] = rule
        else:
            rule_schema = RuleSchema.parse(line)
            rules_schemas[rule_schema.id] = rule_schema

    messages: List[str] = [line.strip() for line in stream]

    return rules, rules_schemas, messages


def get_patterns(rules_ids: List[int], rules: Dict[int, Rule]) -> List[str]:
    # if rule consists of 2 sub-rules with multiple patterns then rule patterns would be production of sub-patterns
    # if rule 0 -> rule 1, rule 2
    # and rule 1 patterns = "x", "y"
    # and rule 2 patterns = "z", "w"
    # then rule 0 patterns= "xz", "xw", "yz", "wy"
    if not rules_ids:
        return []

    combinations = [rules[rule_id].patterns for rule_id in rules_ids]
    return ["".join(pattern) for pattern in list(product(*combinations))]


def build_patterns_from_schema(rule_schema: RuleSchema, rules: Dict[int, Rule], rules_schemas: Dict[int, RuleSchema]):
    # recursively build all sub-rules if they do not contain patterns
    for rule_id in chain(rule_schema.rule1, rule_schema.rule2):
        if rule_id not in rules:
            rules = build_patterns_from_schema(rules_schemas[rule_id], rules, rules_schemas)

    patterns1 = get_patterns(rule_schema.rule1, rules)
    patterns2 = get_patterns(rule_schema.rule2, rules)
    all_patterns = list(chain(patterns1, patterns2))

    rule = Rule(rule_schema.id, all_patterns)
    rules[rule.id] = rule

    return rules


def calc1(rules: Dict[int, Rule], rules_schemas: Dict[int, RuleSchema]) -> Dict[int, Rule]:
    # all we have to do is parse all schemas from bottom to top and create patterns from rules
    return build_patterns_from_schema(rules_schemas[0], rules, rules_schemas)


def is_valid(message: str, prefixes: Set[str], suffixes: Set[str]) -> bool:
    # check if first part of the message consists only from prefixes patterns
    prefixes_num = 0
    start = 0
    while start < len(message):
        for prefix in prefixes:
            if message.startswith(prefix, start):
                start += len(prefix)
                prefixes_num += 1
                break
        else:
            break

    # check if last part of the message consists only from suffixes patterns
    suffixes_num = 0
    while start < len(message):
        for suffix in suffixes:
            if message.endswith(suffix, start):
                suffixes_num += 1
                start += len(suffix)
                break
        else:
            break
    # if message is valid it should not contain any other symbols
    # and number of prefixes is at least 2, number of suffixes is at least 1 and less than number of prefixes
    return start == len(message) and prefixes_num > suffixes_num >= 1


def calc2(rules: Dict[int, Rule], messages: List[str]) -> int:
    # here we have to replace two rules "8: 42 | 42 8" instead of "8: 42"
    # and "11: 42 31 | 42 11 31" instead of "11: 42 31"
    # but we won't do it actually.
    # new rules contains links to themselves and thus infinite loops would not allow to calc all possible patterns
    #
    # the only higher level rule which depends on rules 8 and 11 is the root rule "0: 8 11"
    # let's try to analyze what the loop "8: 42 | 42 8" actually means
    # for example rule 42 contains of ['a', 'b'] patterns
    # in first loop iteration we should add patterns which are product of initial patterns - ['aa', 'ab', 'ba', 'bb']
    # so the result is ['a', 'b', 'aa', 'ab', 'ba', 'bb']
    # in the second loop will add all permutation of 3 elements from 'aaa' to 'bbb' and 4 elements 'aaaa' - 'bbbb'
    # instead of endless generation we'll derive a rule:
    # rule 8 patterns consist of all possible combinations of rule 42 patterns and nothing more
    #
    # second replacement is a bit trickier - "11: 42 31 | 42 11 31"
    # again, for example rule 42 contains of ['a', 'b'] patterns. rule 31 - of ['x', 'y']
    # on first iteration rule 11 consists of product of 2 rules - ['aX', 'aY', 'bX', 'bY']
    # on the second iteration we'll add product of 3 rules - 42 11 31:
    # ['aaXX', 'aaXY', 'aaYX', 'aaYY', 'abXX', 'abXY', 'abYX', 'abYY', 'baXX', 'baXY', 'baYX', 'baYY', 'bbXX', 'bbXY', 'bbYX', 'bbYY']
    # and here goes general rule for 11:
    # rule 11 patterns consist of any combinations of rule 42 patterns plus the same number of combinations of rule 31 patterns
    # so any zero rule pattern can be defined as junction of:
    # - n patterns of 42 rule plus
    # - m patterns of 42 rule plus
    # - m patterns of 31 rule plus
    # where n and m any positive numbers
    # this works only if all patterns are unique

    rule_prefix = set(rules[42].patterns)
    rule_suffix = set(rules[31].patterns)
    return sum(is_valid(message, rule_prefix, rule_suffix) for message in messages)


if __name__ == "__main__":
    initial_rules, initial_rules_schemas, initial_messages = read_data(sys.stdin)

    rules_with_patterns = calc1(initial_rules, initial_rules_schemas)
    zero_rule = rules_with_patterns[0]
    patterns = set(zero_rule.patterns)
    print(f"result 1: {sum(message in patterns for message in initial_messages)}")

    res2 = calc2(rules_with_patterns, initial_messages)
    print(f"result 2: {res2}")
