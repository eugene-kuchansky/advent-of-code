import sys
from typing import List, Iterable, Dict


class BagsRepo:
    def __init__(self):
        self.repo: Dict[str, Bag] = {}

    def get(self, color: str) -> "Bag":
        if color in self.repo:
            bag = self.repo[color]
        else:
            bag = Bag(color)
            self.repo[color] = bag
        return bag


class Bag:
    def __init__(self, color: str):
        self.color = color
        self.contains: Dict[Bag, int] = {}
        self.in_bags: List[Bag] = []

    def add_inner_bug(self, inner_bag: "Bag", num: int):
        self.contains[inner_bag] = num

    def add_container(self, outer_bag: "Bag"):
        self.in_bags.append(outer_bag)

    def __hash__(self) -> int:
        return hash(str(self.color))

    def __eq__(self, other) -> bool:
        return isinstance(other, Bag) and self.color == other.color

    def __str__(self) -> str:
        str_ = f"Color: {self.color}"

        inner_bags = ", ".join(f"{num} {bag.color}" for bag, num in self.contains.items())
        if not inner_bags:
            inner_bags = "nothing"
        str_ = f"{str_}, inner bags: {inner_bags}"

        outer_bags = ", ".join(f"{bag.color}" for bag in self.in_bags)
        if not outer_bags:
            outer_bags = "no bags"
        str_ = f"{str_}, in bags: {outer_bags}"

        return str_

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def create_from_str(value: str, bags_repo: BagsRepo):
        color, rest = value.split(" bags contain ")
        bag = bags_repo.get(color)

        if rest == "no other bags":
            return bag

        for inner_bag in rest.split(", "):
            num, color1, color2, bag_word = inner_bag.split(" ")
            inner_color = f"{color1} {color2}"
            inner_bag = bags_repo.get(inner_color)
            bag.add_inner_bug(inner_bag, int(num))
            inner_bag.add_container(bag)


def read_data(stream: Iterable[str]) -> BagsRepo:
    bags_repo = BagsRepo()
    for line in stream:
        Bag.create_from_str(line.strip(".\n"), bags_repo)
    return bags_repo


def calc1(bags_repo: BagsRepo) -> int:
    initial_bag = bags_repo.get("shiny gold")
    counted_bags = set()
    num = 0
    q = []

    for outer_bag in initial_bag.in_bags:
        q.append(outer_bag)

    while q:
        bag = q.pop()
        if bag not in counted_bags:
            counted_bags.add(bag)
            num += 1
            for outer_bag in bag.in_bags:
                q.append(outer_bag)
    return num


def calc2(bags_repo: BagsRepo) -> int:
    initial_bag = bags_repo.get("shiny gold")
    num = 0
    q = [(1, initial_bag)]

    while q:
        multiplier, bag = q.pop()
        for inner_bag, inner_num in bag.contains.items():
            inner_bags_num = multiplier * inner_num
            q.append((inner_bags_num, inner_bag))
            num += inner_bags_num
    return num


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
