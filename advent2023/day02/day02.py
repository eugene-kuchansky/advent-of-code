import sys
from typing import List
from dataclasses import dataclass


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


@dataclass
class Subset:
    red: int
    green: int
    blue: int

    @classmethod
    def parse(cls, info):
        colors = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for color_info in info.strip().split(", "):
            num, color = color_info.strip().split(" ")
            colors[color] = int(num)

        return cls(**colors)

    def __gt__(self, other_subset: "Subset"):
        return self.red > other_subset.red or self.green > other_subset.green or self.blue > other_subset.blue

    def max(self, other_subset: "Subset"):
        return Subset(
            red=max(self.red, other_subset.red),
            green=max(self.green, other_subset.green),
            blue=max(self.blue, other_subset.blue),
        )

    def power(self):
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    subsets: List[Subset]

    @classmethod
    def parse(cls, line):
        game_info, subsets_info = line.split(":")
        _, num = game_info.split(" ")
        subsets = []
        for subset_info in subsets_info.split(";"):
            subset = Subset.parse(subset_info)
            subsets.append(subset)

        return cls(int(num), subsets)


def parse(lines: List[str]) -> List[Game]:
    games = []
    for line in lines:
        game = Game.parse(line)
        games.append(game)

    return games


def calc1(games: List[Game]) -> int:
    max_subset = Subset(red=12, green=13, blue=14)
    result = 0
    for game in games:
        for subset in game.subsets:
            if subset > max_subset:
                break
        else:
            result += game.id

    return result


def calc2(games: List[Game]) -> int:
    result = 0
    for game in games:
        max_subset = Subset(red=0, green=0, blue=0)
        for subset in game.subsets:
            max_subset = max_subset.max(subset)
        result += max_subset.power()
    return result


if __name__ == "__main__":
    raw_data = read_data()
    games = parse(raw_data)
    print(calc1(games))
    print(calc2(games))
