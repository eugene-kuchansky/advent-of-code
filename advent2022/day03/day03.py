import sys
import string


def read_data():
    rucksacks = [line.rstrip() for line in sys.stdin]
    return rucksacks


def calc_priority(letter):
    if letter in string.ascii_lowercase:
        first_letter = ord("a") - 1
    else:
        first_letter = ord("A") - 27
    priority = ord(letter) - first_letter
    return priority


def calc1(data):
    priorities = 0
    for rucksack in data:
        middle = len(rucksack) // 2
        part1 = rucksack[:middle]
        part2 = rucksack[middle:]
        commons = set.intersection(set(part1), set(part2))
        priorities += calc_priority(commons.pop())
    return priorities


def by_chunk(iterable, size=3):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def calc2(data):
    priorities = 0
    for rucksacks in by_chunk(data, 3):
        commons = set.intersection(*[set(r) for r in rucksacks])
        priorities += calc_priority(commons.pop())
    return priorities


if __name__ == "__main__":
    raw_data = read_data()

    print(calc1(raw_data))
    print(calc2(raw_data))
