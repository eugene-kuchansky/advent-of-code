import sys
from typing import List, Tuple


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Tuple[List[List[int]], List[List[int]]]:
    winning_numbers = []
    player_numbers = []
    for line in lines:
        _, numbers = line.split(":")
        winning_part, player_part = numbers.split(" | ")
        winning_numbers.append([int(n) for n in winning_part.strip().split(" ") if n])
        player_numbers.append([int(n) for n in player_part.strip().split(" ") if n])
    return winning_numbers, player_numbers


def calc_score(winning: List[int], player: List[int]) -> int:
    common = set(winning).intersection(set(player))
    return len(common)


def calc1(winning_numbers: List[List[int]], player_numbers: List[List[int]]) -> int:
    result = 0
    for winning, player in zip(winning_numbers, player_numbers):
        score = calc_score(winning, player)
        if score:
            result += 2 ** (score - 1)
    return result


def calc2(winning_numbers: List[List[int]], player_numbers: List[List[int]]) -> int:
    cards_num = len(winning_numbers)
    cards = [1 for _ in range(cards_num)]

    for line, (winning, player) in enumerate(zip(winning_numbers, player_numbers)):
        score = calc_score(winning, player)
        if score:
            for next_line in range(line + 1, line + min(score, cards_num - 1) + 1):
                cards[next_line] += cards[line]

    return sum(cards)


if __name__ == "__main__":
    raw_data = read_data()
    winning_numbers, player_numbers = parse(raw_data)
    print(calc1(winning_numbers, player_numbers))
    print(calc2(winning_numbers, player_numbers))
