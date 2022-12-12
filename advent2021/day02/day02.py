import sys


def read_data():
    data = [line.split() for line in sys.stdin]
    return [(command, int(value)) for command, value in data]


def calc1(data):
    horizontal = 0
    depth = 0
    for command, value in data:
        if command == "forward":
            horizontal += value
        elif command == "down":
            depth += value
        elif command == "up":
            depth -= value
    return horizontal * depth


def calc2(data):
    horizontal = 0
    depth = 0
    aim = 0
    for command, value in data:
        if command == "forward":
            horizontal += value
            depth += aim * value
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value
    return horizontal * depth


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
