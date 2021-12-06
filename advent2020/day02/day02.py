import sys
from collections import namedtuple
from typing import List

PasswordRecord = namedtuple("PasswordRecord", "min_limit max_limit symbol password")


def read_data() -> List[PasswordRecord]:
    res = []
    for line in sys.stdin:
        rule, password = [_.strip() for _ in line.split(":")]
        limits, symbol = rule.split(" ")
        min_limit, max_limit = limits.split("-")
        res.append(PasswordRecord(int(min_limit), int(max_limit), symbol, password))
    return res


def calc1(data: List[PasswordRecord]) -> int:
    total_valid = 0
    for record in data:
        cnt = record.password.count(record.symbol)
        is_password_valid = record.min_limit <= cnt <= record.max_limit
        total_valid += int(is_password_valid)
    return total_valid


def calc2(data: List[PasswordRecord]) -> int:
    total_valid = 0
    for record in data:
        symbol1 = record.password[record.min_limit - 1]
        symbol2 = record.password[record.max_limit - 1]
        is_password_valid = bool(symbol1 == record.symbol) ^ bool(symbol2 == record.symbol)
        total_valid += int(is_password_valid)
    return total_valid


if __name__ == "__main__":
    raw_data = read_data()
    res1 = calc1(raw_data)
    print(f"result 1: {res1}")
    res2 = calc2(raw_data)
    print(f"result 2: {res2}")
