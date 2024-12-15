import sys


def read_data() -> list[dict[str, int]]:
    raw_data = sys.stdin.read()
    equations = []
    spam = len("Button X: ")
    for eq in raw_data.strip().split("\n\n"):
        a, b, result = eq.split("\n")
        a_x_y = a[spam:].split(", ")
        b_x_y = b[spam:].split(", ")

        a_x, a_y = int(a_x_y[0][2:]), int(a_x_y[1][2:])
        b_x, b_y = int(b_x_y[0][2:]), int(b_x_y[1][2:])

        result_x_y = result[len("Prize: ") :].split(", ")
        result_x, result_y = int(result_x_y[0][2:]), int(result_x_y[1][2:])

        equations.append(
            {
                "a_x": a_x,
                "a_y": a_y,
                "b_x": b_x,
                "b_y": b_y,
                "result_x": result_x,
                "result_y": result_y,
            }
        )

    return equations


def solve_equation(eq: dict[str, int]) -> tuple[float, float]:
    e1 = (eq["a_x"] * eq["a_y"], eq["b_x"] * eq["a_y"], eq["result_x"] * eq["a_y"])
    e2 = (eq["a_y"] * eq["a_x"], eq["b_y"] * eq["a_x"], eq["result_y"] * eq["a_x"])

    b = (e2[2] - e1[2]) / (e2[1] - e1[1])
    a = (eq["result_x"] - b * eq["b_x"]) / eq["a_x"]
    return a, b


def calc1(equations: list[dict[str, int]]) -> int:
    result = 0
    for eq in equations:
        a, b = solve_equation(eq)
        if a.is_integer() and b.is_integer():
            result += int(a) * 3 + int(b) * 1

    return result


def calc2(equations: list[dict[str, int]]) -> int:
    result = 0
    result = 0
    for eq in equations:
        new_eq = dict(eq)
        new_eq["result_x"] = new_eq["result_x"] + 10000000000000
        new_eq["result_y"] = new_eq["result_y"] + 10000000000000
        a, b = solve_equation(new_eq)
        if a.is_integer() and b.is_integer():
            result += int(a) * 3 + int(b) * 1

    return result


if __name__ == "__main__":
    equations = read_data()
    print(calc1(equations))
    print(calc2(equations))
