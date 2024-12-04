import re
import sys


def read_data() -> list[str]:
    raw_data = sys.stdin.read()
    result = []
    for line in raw_data.split("\n"):
        if not line:
            continue
        result.append(line)
    return result


def calc1(raw_data):
    result = 0
    for line in raw_data:
        numbers = re.findall(r"mul\(([0-9]+),([0-9]+)\)", line)
        for num1, num2 in numbers:
            result += int(num1) * int(num2)
    return result


def calc2(raw_data):
    result = 0
    allow = True
    for line in raw_data:
        operations = re.findall(r"(?:mul\(\d+,\d+\))|don\'t\(\)|do\(\)", line)
        for operation in operations:
            if operation == "don't()":
                allow = False
            elif operation == "do()":
                allow = True
            elif allow:
                numbers = re.search(r"mul\(([0-9]+),([0-9]+)\)", operation).groups(0)
                result += int(numbers[0]) * int(numbers[1])
    return result


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
