import sys


def read_data():
    return [int(line) for line in sys.stdin]


def calc1(data):
    return sum(data[i] < data[i + 1] for i in range(len(data) - 1))


def calc2(data):
    return sum(data[i] < data[i + 3] for i in range(len(data) - 3))


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
