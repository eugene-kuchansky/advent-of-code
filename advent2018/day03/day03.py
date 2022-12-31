import sys
from typing import List, NamedTuple


class Rect(NamedTuple):
    id: int
    col: int
    row: int
    w: int
    h: int


def read_data() -> List[Rect]:
    raw_data = sys.stdin.read()
    rectangles = []
    for item in raw_data.split("\n"):
        id_data, _, pos_data, size_data = item.split(" ")
        _, id_ = id_data.split("#")
        col, row = pos_data[:-1].split(",")
        w, h = size_data.split("x")
        rectangles.append(Rect(int(id_), int(col), int(row), int(w), int(h)))

    return rectangles


def calc1(data: List[Rect]) -> int:
    fabric: List[List[List[int]]] = []
    for _ in range(1000):
        row = [[] for _ in range(1000)]
        fabric.append(row)
    for rect in data:
        for w in range(rect.w):
            for h in range(rect.h):
                fabric[rect.row + h][rect.col + w].append(rect.id)
    res = 0
    for row in fabric:
        for col in row:
            res += int(len(col) >= 2)
    return res


def calc2(data: List[Rect]) -> int:
    fabric: List[List[List[int]]] = []
    for _ in range(1000):
        row = [[] for _ in range(1000)]
        fabric.append(row)
    rects = set(rect.id for rect in data)
    for rect in data:
        for w in range(rect.w):
            for h in range(rect.h):
                point = fabric[rect.row + h][rect.col + w]
                point.append(rect.id)
                if len(point) > 1:
                    for id_ in point:
                        if id_ in rects:
                            rects.remove(id_)
    return list(rects)[0]


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
