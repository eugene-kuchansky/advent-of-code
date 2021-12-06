from itertools import cycle
from collections import deque

def read_data():
    with open("input_data/16.txt") as f:
        raw_data = f.read()
    # raw_data = "80871224585914546619083218645595"
    #raw_data = "12345678"
    return [int(value) for value in raw_data]

PATTERN = [0, 1, 0, -1]


class PatternGen(object):
    def __init__(self, num):
        self.num = num
        self.patterns = self._gen()

    def _gen(self):
        patterns = []
        for i in range(self.num):
            pattern = []
            for n in PATTERN:
                for j in range(i + 1):
                    pattern.append(n)
            d = deque(pattern)
            d.rotate(-1)
            pattern = list(d)
            while len(pattern) < self.num:
                pattern = pattern * 2
            pattern = pattern[:self.num]
            patterns.append(pattern)

        return patterns

    def get_pattern(self, i):
        return cycle(self.patterns[i])


def calc(numbers, pattern_gen):
    new_numbers = []
    for i in range(len(numbers)):
        res = 0
        pattern = pattern_gen.get_pattern(i)
        for num, k in zip(numbers, pattern):
            # print("num", num, "k", k)
            if k:
                res += (num * k) % 10
        res = abs(res)
        new_numbers.append(res)
    return new_numbers


def part1():
    numbers = read_data()
    # print("data", numbers)
    # print()
    pattern_gen = PatternGen(len(numbers))
    # for pattern in pattern_gen.patterns:
    #     print(pattern)
    # print()
    for _ in range(100):
        numbers = calc(numbers, pattern_gen)
    print("".join(str(_) for _ in numbers[:8]))


def calc2(numbers):
    new_numbers = []
    new_numbers.append(sum(numbers) % 10)
    for i in range(1, len(numbers)):
        n = abs((new_numbers[i - 1] - numbers[i - 1]) % 10)
        new_numbers.append(n)
    #new_numbers = [n % 10 for n in new_numbers]
    return new_numbers


def part2():
    numbers = read_data()
    start_num = int("".join(str(_) for _ in numbers[:7]))

    real_signal = []
    for _ in range(10000):
        real_signal.extend(numbers)

    numbers = real_signal[start_num:]

    for _ in range(100):
        numbers = calc2(numbers)
    print("".join(str(_) for _ in numbers[:8]))

"""
85600369

orig pattern= 0 1 0 -1

6500000
5 971 509

1  + 0  + -1 + 0  + 1  + 0  + -1 + 0  = 4
0  + 1  + 1  + 0  + 0  + -1 + -1 + 0  = 8
0  + 0  + 1  + 1  + 1  + 0  + 0  + 0  = 2
0  + 0  + 0  + 1  + 1  + 1  + 1  + 0  = 2
0  + 0  + 0  + 0  + 1  + 1  + 1  + 1  = 6
0  + 0  + 0  + 0  + 0  + 1  + 1  + 1  = 1
0  + 0  + 0  + 0  + 0  + 0  + 1  + 1  = 5
0  + 0  + 0  + 0  + 0  + 0  + 0  + 1  = 8
"""

if __name__ == "__main__":
    part2()
