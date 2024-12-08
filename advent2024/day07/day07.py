import sys


def read_data() -> list[tuple[int, list[int]]]:
    raw_data = sys.stdin.read()

    equations = []

    for line in raw_data.strip().split("\n"):
        result, numbers = line.split(":")
        numbers = list(map(int, numbers.split()))
        equations.append((int(result), numbers))

    return equations


def solve_equation(result: int, numbers: list[int], operations: str, solution: int) -> bool:
    if result > solution:
        return False

    for operator in operations:
        if operator == "*":
            new_result = result * numbers[0]
        elif operator == "+":
            new_result = result + numbers[0]
        elif operator == "|":
            new_result = int(str(result) + str(numbers[0]))

        if len(numbers) == 1:
            if new_result == solution:
                return True
        elif solve_equation(new_result, numbers[1:], operations, solution):
            return True

    return False


def calc1(equations: list[tuple[int, list[int]]]) -> int:
    result = 0
    for solution, numbers in equations:
        if solve_equation(numbers[0], numbers[1:], "+*", solution):
            result += solution
    return result


def calc2(equations: list[tuple[int, list[int]]]) -> int:
    result = 0
    for solution, numbers in equations:
        if solve_equation(numbers[0], numbers[1:], "+*|", solution):
            result += solution
    return result


if __name__ == "__main__":
    numbers = read_data()
    print(calc1(numbers))
    print(calc2(numbers))
