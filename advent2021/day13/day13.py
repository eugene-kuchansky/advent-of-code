from typing import List, Tuple, Set
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


@dataclass(frozen=True)
class Dot:
    x: int
    y: int


Dots = Set[Dot]


@dataclass
class Fold:
    line: str
    value: int


def parse(raw: str) -> Tuple[Dots, List[Fold]]:
    dots: Dots = set()
    folds: List[Fold] = []

    for line in raw.splitlines():
        if not line:
            continue
        if line.startswith("fold along"):
            words = line.split(" ")
            line, raw_value = words[-1].split("=")
            folds.append(Fold(line, int(raw_value)))
        else:
            x, y = line.split(",")
            dots.add(Dot(int(x), int(y)))

    return dots, folds


def fold_paper(dots: Dots, fold: Fold) -> Dots:
    new_dots: Dots = set()
    if fold.line == "x":
        for dot in dots:
            if dot.x < fold.value:
                new_dots.add(dot)
            elif dot.x > fold.value:
                new_x = 2 * fold.value - dot.x
                assert new_x >= 0
                new_dots.add(Dot(new_x, dot.y))
    else:
        for dot in dots:
            if dot.y < fold.value:
                new_dots.add(dot)
            elif dot.y > fold.value:
                new_y = 2 * fold.value - dot.y
                assert new_y >= 0
                new_dots.add(Dot(dot.x, new_y))

    return new_dots


def display_dots(dots) -> str:
    max_x = 0
    max_y = 0
    for dot in dots:
        if max_x < dot.x:
            max_x = dot.x
        if max_y < dot.y:
            max_y = dot.y
    matrix = [["." for x in range(max_x + 1)] for y in range(max_y + 1)]
    for dot in dots:
        matrix[dot.y][dot.x] = "#"
    return "\n".join(["".join(row) for row in matrix])


def calc(dots: Dots, folds: List[Fold]) -> int:
    dots = fold_paper(dots, folds[0])
    return len(dots)


def calc2(dots: Dots, folds: List[Fold]) -> str:
    for fold in folds:
        dots = fold_paper(dots, fold)
    return display_dots(dots)


assert calc(*parse(RAW)) == 17


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(*parse(raw_data)))
    print(calc2(*parse(raw_data)))
