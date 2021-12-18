from typing import Tuple


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


def parse(raw: str) -> Tuple[int, int, int, int]:
    x_part, y_part = raw.replace("target area: ", "").split(", ")
    min_x, max_x = [int(_) for _ in x_part.replace("x=", "").split("..")]
    min_y, max_y = [int(_) for _ in y_part.replace("y=", "").split("..")]
    return min_x, max_x, min_y, max_y


def max_y_speed(min_y) -> int:
    # max height - at y steps
    # on falling down at pos == 0 the speed is -y -1
    # to target in range min_y max_y
    #  max_y >= -y -1 >= min_y
    #  -max_y =< y + 1 <= -min_y
    #  -max_y -1 =< y <= -min_y - 1
    return -min_y - 1


def calc(min_x, max_x, min_y, max_y) -> int:
    y_high_value = max_y_speed(min_y)
    max_height = y_high_value ** 2 - y_high_value * (y_high_value - 1) // 2
    return max_height


def calc2(min_x, max_x, min_y, max_y) -> int:
    all_x = range(1, max_x + 1)
    all_y = range(min_y, max_y_speed(min_y) + 1)
    total = 0

    # ugly brute-force
    for x in all_x:
        for y in all_y:
            if hit(x, y, min_x, max_x, min_y, max_y):
                total += 1
    return total


def hit(x, y, min_x, max_x, min_y, max_y) -> bool:
    pos_x = 0
    pos_y = 0
    while True:
        if max_x >= pos_x >= min_x and max_y >= pos_y >= min_y:
            return True
        if x > max_x or y < min_y:
            return False
        pos_x += x
        pos_y += y

        if x:
            x -= 1
        y -= 1
    return False


RAW = "target area: x=20..30, y=-10..-5"
assert calc(*parse(RAW)) == 45
assert calc2(*parse(RAW)) == 112


if __name__ == "__main__":
    raw = read_data()
    print(calc(*parse(raw)))
    print(calc2(*parse(raw)))
