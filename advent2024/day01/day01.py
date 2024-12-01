import sys
from collections import Counter


def read_data() -> list[str]:
    raw_data = sys.stdin.read()
    list1 = []
    list2 = []
    for line in raw_data.split("\n"):
        if not line:
            continue
        nums = line.split("   ")
        list1.append(int(nums[0]))
        list2.append(int(nums[1]))
    return list1, list2


def calc1(raw_data):
    list1, list2 = raw_data
    result = 0
    for n1, n2 in zip(sorted(list1), sorted(list2)):
        result += abs(n1 - n2)
    return result


def calc2(raw_data):
    list1, list2 = raw_data
    result = 0
    numbers2 = Counter(list2)
    for n1 in list1:
        result += n1 * numbers2[n1]
    return result


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
