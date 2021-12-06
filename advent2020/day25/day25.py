import sys
from typing import Iterable, Tuple


def read_data(stream: Iterable[str]) -> Tuple[int, int]:
    lines = [line.strip() for line in stream]
    pub_key1 = int(lines[0])
    pub_key2 = int(lines[1])
    return pub_key1, pub_key2


def find_enc_key(loop: int, pub_key: int, divider: int) -> int:
    enc_key = pub_key
    for _ in range(loop):
        enc_key = enc_key * pub_key % divider
    return enc_key


def find_loop(pub_key: int, divider: int) -> int:
    loop = 0
    num = 1
    subj = 7
    while True:
        num = (num * subj) % divider
        if num == pub_key:
            break
        loop += 1
    return loop


def calc1(pub_key1: int, pub_key2: int) -> int:
    divider = 20201227

    loop1 = find_loop(pub_key1, divider)
    loop2 = find_loop(pub_key2, divider)

    enc_key1 = find_enc_key(loop2, pub_key1, divider)
    enc_key2 = find_enc_key(loop1, pub_key2, divider)

    if enc_key1 != enc_key2:
        raise RuntimeError("wups")

    return enc_key1


if __name__ == "__main__":
    keys = read_data(sys.stdin)

    res = calc1(*keys)
    print(f"result 1: {res}")
