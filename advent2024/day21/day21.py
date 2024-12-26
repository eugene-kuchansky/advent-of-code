import sys
from functools import lru_cache
from itertools import permutations


def read_data() -> list[str]:
    raw_data = sys.stdin.read()
    codes = []
    for line in raw_data.strip().split("\n"):
        codes.append(list(line))

    return codes


NUMPAD = (
    ("7", (0, 0)),
    ("8", (1, 0)),
    ("9", (2, 0)),
    ("4", (0, 1)),
    ("5", (1, 1)),
    ("6", (2, 1)),
    ("1", (0, 2)),
    ("2", (1, 2)),
    ("3", (2, 2)),
    ("0", (1, 3)),
    ("A", (2, 3)),
)

KEYPAD = (
    ("^", (1, 0)),
    ("A", (2, 0)),
    ("<", (0, 1)),
    ("v", (1, 1)),
    (">", (2, 1)),
)


DIR_TO_DELTA = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1),
}


@lru_cache(maxsize=None)
def shortest_paths(pad: tuple[tuple[str, tuple[int, int]], ...], from_key: str, to_key: str) -> list[list[str]]:
    if from_key == to_key:
        return [["A"]]

    pad_dict = {k: v for k, v in pad}
    valid_positions = set(pad_dict.values())

    from_pos = pad_dict[from_key]
    to_pos = pad_dict[to_key]

    dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]

    paths = []

    dx_dir = ">"
    dy_dir = "v"
    if dx < 0:
        dx_dir = "<"

    if dy < 0:
        dy_dir = "^"

    seq = [dx_dir] * abs(dx) + [dy_dir] * abs(dy)
    for directions in set(permutations(seq)):
        pos = from_pos
        path = []
        for direction in directions:
            delta = DIR_TO_DELTA[direction]
            pos = (pos[0] + delta[0], pos[1] + delta[1])
            if pos not in valid_positions:
                break
            path.append(direction)
        else:
            path.append("A")
            paths.append(path)
    return paths


@lru_cache(maxsize=None)
def get_path_len(path: str, depth: int, pad) -> int:
    result = 0
    prev_key = "A"
    for key in path:
        partial_paths = shortest_paths(pad, prev_key, key)
        prev_key = key
        if depth == 0:
            result += min(len(_) for _ in partial_paths)
        else:
            result += min(get_path_len("".join(partial_path), depth - 1, KEYPAD) for partial_path in partial_paths)
    return result


def calc1(codes: list[list[str]]) -> int:
    result = 0

    for code in codes:
        path_len = get_path_len("".join(code), 2, NUMPAD)
        result += path_len * int("".join(code[:-1]))

    return result


def calc2(codes: list[list[str]]) -> int:
    result = 0
    for code in codes:
        path_len = get_path_len("".join(code), 25, NUMPAD)
        result += path_len * int("".join(code[:-1]))

    return result


if __name__ == "__main__":
    codes = read_data()
    print(calc1(codes))
    print(calc2(codes))
