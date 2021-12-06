import sys
from collections import defaultdict


def read_data():
    return [int(line) for line in sys.stdin]


def get_data_map(data):
    data_map = defaultdict(list)
    for i, num in enumerate(data):
        data_map[num].append(i)
    return data_map


def calc1(data, data_map, target_value, start_pos):
    for pos1, value1 in enumerate(data[:-1], start_pos):
        value2 = target_value - value1
        if value2 not in data_map:
            continue
        for pos2 in data_map[value2]:
            if pos2 + start_pos > pos1:
                return value1, value2
    return None


def calc2(data, data_map, target_value):
    for pos1, value1 in enumerate(data[:-2]):
        sub_target_value = target_value - value1
        sub_start_pos = pos1 + 1
        sub_res = calc1(data[sub_start_pos:], data_map, sub_target_value, sub_start_pos)
        if sub_res:
            return value1, sub_res[0], sub_res[1]
    return None


if __name__ == "__main__":
    raw_data = read_data()
    sum_target_value = 2020
    values_data_map = get_data_map(raw_data)
    res1 = calc1(raw_data, values_data_map, sum_target_value, start_pos=0)
    if res1:
        print("result 1:", res1[0] * res1[1])
    else:
        print("result 1: err")

    res2 = calc2(raw_data, values_data_map, sum_target_value)
    if res2:
        print("result 2:", res2[0] * res2[1] * res2[2])
    else:
        print("result 2: err")
