import sys
from math import trunc


def read_data() -> tuple[int, int, list[int]]:
    raw_data = sys.stdin.read()

    registers_data, program_data = raw_data.strip().split("\n\n")
    registers = registers_data.split("\n")
    a = int(registers[0].split(": ")[1])
    b = int(registers[1].split(": ")[1])
    c = int(registers[2].split(": ")[1])
    program = [int(code) for code in program_data.split(": ")[1].split(",")]

    return a, b, c, program


def run_program(a: int, b: int, c: int, program: list[int]) -> int:
    reg_a, reg_b, reg_c = 4, 5, 6
    # operand_name = {reg_a: "a", reg_b: "b", reg_c: "c"}
    registers = {reg_a: a, reg_b: b, reg_c: c, 7: None}

    output = []
    i = 0
    while i < len(program) - 1:
        opcode = program[i]
        operand = program[i + 1]

        if opcode == 0:
            # adv
            # (f"adv: reg_a = reg_a // {2 ** operand_name.get(operand, operand)}")
            registers[reg_a] = trunc(registers[reg_a] / 2 ** registers.get(operand, operand))
        elif opcode == 1:
            # bxl
            # (f"bxl: reg_b = reg_b ^ {operand_name.get(operand, operand)}")
            registers[reg_b] = registers[reg_b] ^ operand

        elif opcode == 2:
            # bst
            # (f"bst: reg_b = {operand_name.get(operand, operand)} % 8")
            registers[reg_b] = registers.get(operand, operand) % 8

        elif opcode == 3:
            # jnz
            # ("jnz")
            if registers[reg_a] != 0:
                i = operand - 2

        elif opcode == 4:
            # bxc
            # ("bxc: reg_b = reg_b ^ reg_c")
            registers[reg_b] = registers[reg_b] ^ registers[reg_c]
        elif opcode == 5:
            # out
            # (f"out: {operand_name.get(operand, operand)} % 8")
            output.append(registers.get(operand, operand) % 8)

        elif opcode == 6:
            # bdv
            # hehe, never happened
            registers[reg_b] = registers[reg_a] // 2 ** registers.get(operand, operand)
        elif opcode == 7:
            # cdv
            # (f"cdv: reg_c = reg_a // 2 ** {operand_name.get(operand, operand)}")
            registers[reg_c] = registers[reg_a] // 2 ** registers.get(operand, operand)

        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        i += 2

    return output


def calc1(a: int, b: int, c: int, program: list[int]) -> int:
    result = 0
    output = run_program(a, b, c, program)
    result = ",".join(str(x) for x in output)
    return result


def calc2(a: int, b: int, c: int, program: list[int]) -> int:
    # initial a register value
    a = [0]

    # didko. i've spent 2 days on this problem
    for i in range(len(program)):
        new_a = []
        # try all possible last digits of a last digit.
        # it can be 0-7, octo number because we have 3 bits in the result
        for a_last_digit in range(8):
            for x in a:
                # run program with current a register value to get the the last digits of the output
                output = run_program(x * 8 + a_last_digit, b, c, program)
                if output[0] == program[len(program) - i - 1]:
                    new_a.append(x * 8 + a_last_digit)
        a = new_a
    for v in sorted(a):
        if run_program(v, b, c, program) == program:
            result = v
            break

    return result


if __name__ == "__main__":
    a, b, c, program = read_data()
    print(calc1(a, b, c, program))
    print(calc2(a, b, c, program))
