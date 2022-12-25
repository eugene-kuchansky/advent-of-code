import sys
from typing import List
import re


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    snafu = raw_data.split("\n")
    return snafu


def int_to_pental(num_10) -> str:
    base = 5
    if num_10 == 0:
        return "0"
    pental = []
    while num_10:
        pental.append(str(num_10 % base))
        num_10 = num_10 // 5

    return "".join(pental[::-1])


def pental_to_int(num_5: str) -> int:
    degree = 0
    num = 0
    base = 5
    for digit in num_5[::-1]:
        num += int(digit) * base**degree
        degree += 1
    return num


def snafu_to_pental(match) -> str:
    snafu = match.group()

    if "-" in snafu:
        return int_to_pental(pental_to_int(snafu.replace("-", "0")) - 1)
    return int_to_pental(pental_to_int(snafu.replace("=", "0")) - 2)


def pental_to_snafu(match) -> str:
    pental = match.group()
    if "3" == pental[-1]:
        return "".join([int_to_pental(pental_to_int(pental) + 2)[:-1], "="])
    return "".join([int_to_pental(pental_to_int(pental) + 1)[:-1], "-"])


def snafu_to_int(snafu: str) -> int:
    pental = snafu
    while "-" in pental or "=" in pental:
        pental = re.sub(r"\d+[\-|=]", snafu_to_pental, pental, count=1)
    return pental_to_int(pental)


def int_to_snafu(num: int) -> str:
    pental = int_to_pental(num)
    snafu = pental
    while "3" in snafu or "4" in snafu:
        snafu = re.sub(r"(\d*[3|4]{1})", pental_to_snafu, snafu, count=1)
    return snafu


def calc1(snafu: List[str]) -> str:
    s = sum(snafu_to_int(num) for num in snafu)
    return int_to_snafu(s)


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
