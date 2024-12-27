import sys
from collections import defaultdict, deque
from typing import Generator


def read_data() -> list[int]:
    raw_data = sys.stdin.read()
    numbers = []
    for line in raw_data.strip().split("\n"):
        numbers.append(int(line))

    return numbers


def generate_numbers(number: int, count: int) -> Generator[int, None, None]:
    for i in range(count):
        number = ((number << 6) ^ number) % 16777216
        number = ((number >> 5) ^ number) % 16777216
        number = ((number << 11) ^ number) % 16777216
        yield number


def calc1(numbers: list[int]) -> int:
    result = 0

    for number in numbers:
        secret = None
        for value in generate_numbers(number, 2000):
            secret = value
        result += secret

    return result


def calc2(numbers: list[int]) -> int:
    result = 0

    all_sums = defaultdict(int)

    for number in numbers:
        prev_last_digit = number % 10
        last_four_changes = deque(maxlen=4)
        found_seq = set()

        for secret in generate_numbers(number, 2000):
            last_digit = secret % 10
            last_four_changes.append(last_digit - prev_last_digit)
            t = tuple(last_four_changes)
            if len(last_four_changes) == 4 and t not in found_seq:
                found_seq.add(t)
                all_sums[t] += last_digit

            prev_last_digit = last_digit

    result = max(all_sums.values())
    return result


if __name__ == "__main__":
    numbers = read_data()
    print(calc1(numbers))
    print(calc2(numbers))
