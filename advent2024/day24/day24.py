import sys


def read_data() -> tuple[dict[str, int], dict[str, tuple[str, str, str]]]:
    raw_data = sys.stdin.read()
    values = {}
    gates = {}
    values_data, gates_data = raw_data.strip().split("\n\n")

    for v in values_data.split("\n"):
        name, value = v.split(":")
        values[name] = int(value)
    for g in gates_data.split("\n"):
        operation, name = g.split(" -> ")
        var1, operation, var2 = operation.split(" ")
        var1, var2 = sorted([var1, var2])
        gates[name] = (var1, operation, var2)
    return values, gates


def traverse(
    gate: str, values: dict[str, int], gates: dict[str, tuple[str, str, str]], calculated_values: dict[str, int]
) -> int:
    if gate in calculated_values:
        return calculated_values[gate]

    var1, operation, var2 = gates[gate]
    value1 = traverse(var1, values, gates, calculated_values)
    value2 = traverse(var2, values, gates, calculated_values)

    if operation == "AND":
        calculated_values[gate] = value1 & value2
    elif operation == "OR":
        calculated_values[gate] = value1 | value2
    elif operation == "XOR":
        calculated_values[gate] = value1 ^ value2
    return calculated_values[gate]


def calc1(values: dict[str, int], gates: dict[str, tuple[str, str, str]]) -> int:
    result = 0

    calculated_values = dict(values)
    for gate in gates:
        traverse(gate, values, gates, calculated_values)
    final = {}
    for gate in gates:
        if gate[0] == "z":
            final[gate] = calculated_values[gate]

    final = sorted(final.items(), key=lambda x: x[0])

    for i, v in enumerate(final):
        result += v[1] * 2**i

    return result


def traverse_formulas(gate: str, gates: dict[str, tuple[str, str, str]], calculated_values: dict[str, tuple]) -> int:
    if gate in calculated_values:
        return calculated_values[gate]

    if gate not in gates:
        return gate

    var1, operation, var2 = gates[gate]

    value1 = traverse_formulas(var1, gates, calculated_values)
    value2 = traverse_formulas(var2, gates, calculated_values)

    v1, v2 = sorted([value1, value2])

    if operation == "AND":
        calculated_values[gate] = f"({v1} & {v2})"
    elif operation == "OR":
        calculated_values[gate] = f"({v1} | {v2})"
    elif operation == "XOR":
        calculated_values[gate] = f"({v1} ^ {v2})"

    return calculated_values[gate]


def generate_correct_gates():
    # generate correct gates for bitwise calculator for two 45 bit numbers
    # using xor, and, or
    gates = {}

    gates["z00"] = ("x00", "XOR", "y00")  # result
    gates["c00"] = ("x00", "AND", "y00")  # carry

    for i in range(1, 45):
        gates[f"p{i:02}"] = (f"x{i:02}", "XOR", f"y{i:02}")  # partial sum
        gates[f"z{i:02}"] = (f"c{i-1:02}", "XOR", f"p{i:02}")  # result
        gates[f"t{i:02}"] = (f"x{i:02}", "AND", f"y{i:02}")  # carry from sum
        gates[f"s{i:02}"] = (f"p{i:02}", "AND", f"c{i-1:02}")  # carry from previous
        gates[f"c{i:02}"] = (f"t{i:02}", "OR", f"s{i:02}")  # final carry

    # the last carry is the result
    gates["z45"] = gates["c44"]
    del gates["c44"]

    return gates


def calc2(values: dict[str, int], gates: dict[str, tuple[str, str, str]]) -> int:
    result = 0

    correct_gates = generate_correct_gates()
    correct_formulas = {}
    for gate in correct_gates:
        traverse_formulas(gate, correct_gates, correct_formulas)

    mapping = {}
    all_correct = False

    # iterate and fix until all gates are correct
    while not all_correct:
        # generate formulas for current gates
        formulas = {}
        for gate in gates:
            traverse_formulas(gate, gates, formulas)

        # sort formulas by length and value
        # since formulas contain previous formulas, e.g. the length of formula is growing

        ordered_formulas = sorted(formulas.items(), key=lambda x: (len(x[1]), x[1]))
        all_correct = True

        for i, (correct_gate, correct_formula) in enumerate(
            sorted(correct_formulas.items(), key=lambda x: (len(x[1]), x[1]))
        ):
            curr_gate, curr_formula = ordered_formulas[i]

            if curr_formula == correct_formula:
                continue

            # found incorrect formula
            all_correct = False

            op1, _, op2 = gates[curr_gate]
            correct_op1, _, correct_op2 = correct_gates[correct_gate]

            # find correct operator in formula
            if correct_formulas[correct_op1] == formulas[op1] or correct_formulas[correct_op2] == formulas[op1]:
                switch1 = op2
                correct_op = correct_op1
            elif correct_formulas[correct_op1] == formulas[op2] or correct_formulas[correct_op2] == formulas[op2]:
                switch1 = op1
                correct_op = correct_op2
            else:
                print("incorrect", op1, op2)
                exit()

            # find correct operator in previous formulas
            seek_formula = correct_formulas[correct_op]
            for seek_gate, found_formula in formulas.items():
                if found_formula == seek_formula:
                    switch2 = seek_gate
                    break

            gates[switch1], gates[switch2] = gates[switch2], gates[switch1]

            # update mapping in case of replace existing gate
            if switch1 in mapping:
                new_switch1 = mapping[switch1]
                del mapping[switch1]
                del mapping[new_switch1]
                mapping[new_switch1] = switch2
                mapping[switch2] = new_switch1
            elif switch2 in mapping:
                new_switch2 = mapping[switch2]
                del mapping[switch2]
                del mapping[new_switch2]
                mapping[new_switch2] = switch1
                mapping[switch1] = new_switch2
            else:
                mapping[switch1], mapping[switch2] = switch2, switch1
            break

    result = ",".join(sorted(mapping.keys()))

    return result


if __name__ == "__main__":
    values, gates = read_data()
    print(calc1(values, gates))
    print(calc2(values, gates))
