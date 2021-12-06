import sys
from typing import List, Iterable, NamedTuple, Tuple, Set


class Rule(NamedTuple):
    name: str
    lo: Tuple[int, int]
    hi: Tuple[int, int]

    @staticmethod
    def parse_values(rule: str) -> Tuple[int, int]:
        rule_values = [int(_) for _ in rule.split("-")]
        lo, hi = rule_values[0], rule_values[1]
        return lo, hi

    @staticmethod
    def parse(line: str) -> "Rule":
        data = line.split(": ")
        name, rules = data[0], data[1]
        rule1, rule2 = rules.split(" or ")
        lo0, hi0 = Rule.parse_values(rule1)
        lo1, hi1 = Rule.parse_values(rule2)
        return Rule(name, lo=(lo0, lo1), hi=(hi0, hi1))

    def is_valid_field(self, field: int) -> bool:
        return any(
            [
                self.lo[0] <= field <= self.hi[0],
                self.lo[1] <= field <= self.hi[1],
            ]
        )


class Ticket(NamedTuple):
    fields: List[int]

    @staticmethod
    def parse(line: str) -> "Ticket":
        str_values = line.split(",")
        fields = [int(value) for value in str_values]
        return Ticket(fields=fields)


def read_data(stream: Iterable[str]) -> Tuple[List[Rule], List[Ticket], Ticket]:
    rules = []
    for line in stream:
        line = line.strip()
        if not line:
            break
        rule = Rule.parse(line)
        rules.append(rule)

    your_ticket = None
    for line in stream:
        line = line.strip()
        if not line:
            break
        if line == "your ticket:":
            continue
        your_ticket = Ticket.parse(line)

    tickets = []
    for line in stream:
        line = line.strip()
        if not line:
            break
        if line == "nearby tickets:":
            continue
        ticket = Ticket.parse(line)
        tickets.append(ticket)

    return rules, tickets, your_ticket


class Validator:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def get_valid_ticket_rules(self, ticket: Ticket) -> List[Set[Rule]]:
        # return available rules for each ticket's field only if ticket is correct
        ticket_rules: List[Set[Rule]] = []
        for field in ticket.fields:
            # I'd use walrus operator but python version is still 3.6
            available_field_rules = self.get_valid_fields_rules(field)
            if not available_field_rules:
                return []
            ticket_rules.append(available_field_rules)

        return ticket_rules

    def get_valid_fields_rules(self, field: int) -> Set[Rule]:
        return {rule for rule in self.rules if rule.is_valid_field(field)}

    def is_valid_field(self, field: int) -> bool:
        return bool(self.get_valid_fields_rules(field))


def calc1(rules: List[Rule], tickets: List[Ticket]) -> int:
    error_rate = 0
    validator = Validator(rules)

    for ticket in tickets:
        for field in ticket.fields:
            if not validator.get_valid_fields_rules(field):
                error_rate += field

    return error_rate


def get_unique_rules(possible_field_rules) -> Set[Rule]:
    return {list(rules)[0] for rules in possible_field_rules if len(rules) == 1}


def get_fields_rules(possible_field_rules: List[Set[Rule]], unique_rules: Set[Rule]) -> List[Rule]:
    is_updated = True
    while is_updated:
        is_updated = False
        for i, rules in enumerate(possible_field_rules):
            len_rules = len(rules)
            if len_rules > 1:
                rules = rules - unique_rules
                if len(rules) < len_rules:
                    possible_field_rules[i] = rules
                    is_updated = True
                    if len(rules) == 1:
                        unique_rules = unique_rules.union(rules)
    field_rules = []

    for i, rules in enumerate(possible_field_rules):
        # just to be sure
        if len(rules) != 1:
            print("kurwa!")
            exit()
        field_rules.append(list(rules)[0])

    return field_rules


def calc2(rules: List[Rule], tickets: List[Ticket], your_ticket: Ticket) -> int:
    validator = Validator(rules)

    # collect all valid tickets "field->possible rules" into list for each field
    # let's take your ticket consistent rules for each field as initial list
    ticket_rules = validator.get_valid_ticket_rules(your_ticket)
    possible_field_rules: List[Set[Rule]] = [rule for rule in ticket_rules]

    for ticket in tickets:
        ticket_rules = validator.get_valid_ticket_rules(ticket)
        if ticket_rules:
            for i, field_rules in enumerate(ticket_rules):
                possible_field_rules[i] = set.intersection(possible_field_rules[i], field_rules)

    # it might so happen that some ticket can satisfy multiple rules after all
    # take out the rules which definitely describe a field (there is only one rule per field)
    unique_rules = get_unique_rules(possible_field_rules)

    # go through all fields rules and remove the rules that are unique - they unambiguously describe certain fields
    # repeat this process until it is possible remove unique rules from list of ambiguous rules
    fields_rules = get_fields_rules(possible_field_rules, unique_rules)

    departure = 1
    for i, rule in enumerate(fields_rules):
        if rule.name.startswith("departure"):
            departure *= your_ticket.fields[i]

    return departure


if __name__ == "__main__":
    initial_rules, initial_tickets, initial_your_ticket = read_data(sys.stdin)

    res1 = calc1(initial_rules, initial_tickets)
    print(f"result 1: {res1}")

    res2 = calc2(initial_rules, initial_tickets, initial_your_ticket)
    print(f"result 1: {res2}")
