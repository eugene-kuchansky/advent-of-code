import sys
from typing import List, NamedTuple, Iterable, Tuple


class Bus(NamedTuple):
    index: int
    wait: int


def read_data(stream: Iterable[str]) -> Tuple[int, List[Bus]]:
    data = [(line.strip()) for line in stream]
    depart = int(data[0])
    buses = [Bus(ind, int(wait)) for ind, wait in enumerate(data[1].split(",")) if wait != "x"]
    return depart, buses


def calc1(depart: int, buses: List[Bus]) -> int:
    last_buses_time = [depart - depart % bus.wait + bus.wait for bus in buses]
    last_buses_time_with_bus_num = list(zip(last_buses_time, buses))
    earliest = min(last_buses_time_with_bus_num, key=lambda x: x[0])
    bus_time, bus = earliest
    return (bus_time - depart) * bus.wait


# Extended Euclidian algorithm
#   return: Bézout's coefficients and GCD
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# https://en.wikipedia.org/wiki/Bézout%27s_identity
def extended_gcd(a: int, b: int) -> int:
    r_old, r = a, b
    s, s_old = 1, 0
    while r:
        q = r_old // r
        r_old, r = r, r_old - q * r
        s, s_old = s_old, s - q * s_old
    bezout_t = 0 if b == 0 else (r_old - s * a) // b
    # r_old - greatest common divisor
    # bezout_t, s_old - Bézout coefficients
    return bezout_t


def product(args: Iterable[int]) -> int:
    # python 3.6 has no prod function in standard module
    result = 1
    for value in args:
        result *= value
    return result


def calc2(buses: List[Bus]) -> int:
    # Note: I can hardly understand math background around this task
    # The idea and comments are taken from this guy https://github.com/ednl/aoc2020/blob/main/day13.py
    reminders = [-bus.index % bus.wait for bus in buses]
    prod = product(bus.wait for bus in buses)

    # Now do the Chinese whispers
    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    t = 0  # time that satisfies the problem set, but not necessarily the earliest
    for i, bus in enumerate(buses):
        n = prod // bus.wait
        # Second Bézout coefficient is of interest (corresponding to n)
        b2 = extended_gcd(bus.wait, n)
        # and b2 * n = e[i] = M[i] * N[i] from
        # https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Existence_(direct_construction)
        t += reminders[i] * b2 * n

    return t % prod


if __name__ == "__main__":
    depart_info, buses_info = read_data(sys.stdin)
    res1 = calc1(depart_info, buses_info)
    print(f"result 1: {res1}")
    res2 = calc2(buses_info)
    print(f"result 2: {res2}")
