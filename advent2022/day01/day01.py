import sys


def read_data():
    data = [int(line.rstrip()) if line != '\n' else 0 for line in sys.stdin]
    elf = []
    elves = []
    for calories in data:
        if not calories:
            elves.append(sum(elf))
            elf = []
        else:
            elf.append(calories)
    elves.append(sum(elf))
    return elves


def calc1(data):
    return max(data)


def calc2(data):
    return sum(sorted(data, reverse=True)[:3])


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
