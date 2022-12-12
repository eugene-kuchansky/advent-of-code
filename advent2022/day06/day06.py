import sys


def read_data():
    return sys.stdin.read().strip()


def calc1(data):
    for i in range(len(data)):
        if len(set(data[i : i + 4])) == 4:
            return i + 4
    raise ValueError("Not found")


def calc2(data):
    for i in range(len(data)):
        if len(set(data[i : i + 14])) == 14:
            return i + 14
    raise ValueError("Not found")


if __name__ == "__main__":
    raw_data = read_data()

    print(calc1(raw_data))
    print(calc2(raw_data))
