import sys


def read_data():
    data = [line.strip() for line in sys.stdin]
    return [list(value) for value in data]


def calc_gamma_epsilon(data):
    result_ones = [0] * len(data[0])
    total_num = len(data)

    for number in data:
        for i, bit in enumerate(number):
            if bit == "1":
                result_ones[i] += 1
    gamma = ["0"] * len(data[0])
    epsilon = ["0"] * len(data[0])
    for i, num_ones in enumerate(result_ones):
        if 2 * num_ones > total_num:
            gamma[i] = "1"
        else:
            epsilon[i] = "1"
    return gamma, epsilon


def calc1(data):
    gamma, epsilon = calc_gamma_epsilon(data)
    gamma_value = int("".join(gamma), 2)
    epsilon_value = int("".join(epsilon), 2)
    return gamma_value * epsilon_value


def find_by_mask(int_data, bit_shift, take_most_bit):
    data = int_data.copy()
    mask = 1 << bit_shift - 1
    while len(data) != 1:
        num_ones = 0
        for value in data:
            if value & mask:
                num_ones += 1

        if num_ones * 2 > len(data):
            most_bit = take_most_bit
        elif num_ones * 2 < len(data):
            most_bit = not take_most_bit
        else:
            most_bit = take_most_bit
        new_data = []
        for value in data:

            if bool(value & mask) == most_bit:
                new_data.append(value)
        data = new_data
        mask = mask >> 1

    return data[0]


def calc2(data):
    int_data = [int("".join(value), 2) for value in data]
    bit_pos = len(data[0])
    oxygen_rate = find_by_mask(int_data, bit_pos, take_most_bit=1)
    co2_rate = find_by_mask(int_data, bit_pos, take_most_bit=0)
    return oxygen_rate * co2_rate


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
