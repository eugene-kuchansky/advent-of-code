import sys
from typing import List
from dataclasses import dataclass, field
import enum
from collections import defaultdict
from functools import total_ordering


class Value(enum.IntEnum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    Three = 4
    FullHouse = 5
    Four = 6
    Five = 7


J_CARD = 11
JOKER = 0

CARDS_MAP = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


@total_ordering
@dataclass
class Hand:
    cards: List[int]
    bid: int
    value: Value = field(init=False)

    @classmethod
    def from_str(cls, line: str) -> "Hand":
        cards_info, bid_info = line.split(" ")

        cards = [CARDS_MAP[card] for card in cards_info]
        bid = int(bid_info)

        return cls(cards, bid)

    def _pair_cards(self) -> dict[int, int]:
        assert len(self.cards) == 5
        paired = defaultdict(int)
        for card in self.cards:
            paired[card] += 1
        return paired

    def _get_value(self, paired_len: int, max_pairs: int) -> Value:
        if paired_len == 1:
            return Value.Five

        if paired_len == 2:
            if max_pairs == 4:
                return Value.Four
            elif max_pairs == 3:
                return Value.FullHouse
            else:
                raise ValueError("cannot calc value", self.cards)

        if paired_len == 3:
            if max_pairs == 3:
                return Value.Three
            if max_pairs == 2:
                return Value.TwoPair

        if paired_len == 4:
            return Value.OnePair

        if paired_len == 5:
            return Value.HighCard

        raise ValueError("cannot calc value", self.cards)

    def __post_init__(self):
        paired = self._pair_cards()

        paired_len = len(paired)
        max_pairs = max(list(paired.values()))

        self.value = self._get_value(paired_len, max_pairs)

    def __eq__(self, other: "Hand") -> bool:
        return self.value == other.value and self.cards == other.cards

    def __gt__(self, other: "Hand") -> bool:
        if self.value == other.value:
            return self.cards > other.cards
        return self.value > other.value

    def jokerize(self):
        # replace old joker value to the lowest one
        self.cards = [card if card != J_CARD else JOKER for card in self.cards]

        if JOKER not in self.cards or self.value == Value.Five:
            return

        # calc pairs
        paired = self._pair_cards()

        # remove joker from pairs
        joker_num = paired[JOKER]
        del paired[JOKER]

        # calc pairs without jokers number
        paired_len = len(paired)
        max_pairs = max(list(paired.values()))

        # add jokers number to highest pair number
        max_pairs += joker_num

        # recalculate value
        self.value = self._get_value(paired_len, max_pairs)


assert Hand.from_str("AAAAA 0").value == Value.Five
assert Hand.from_str("AA8AA 0").value == Value.Four
assert Hand.from_str("23332 0").value == Value.FullHouse
assert Hand.from_str("TTT98 0").value == Value.Three
assert Hand.from_str("23432 0").value == Value.TwoPair
assert Hand.from_str("A23A4 0").value == Value.OnePair
assert Hand.from_str("23456 0").value == Value.HighCard


h1 = Hand.from_str("32T3K 0")
assert h1.value == Value.OnePair
h1.jokerize()
assert h1.value == Value.OnePair

h2 = Hand.from_str("T55J5 0")
assert h2.value == Value.Three
h2.jokerize()
assert h2.value == Value.Four

h3 = Hand.from_str("JJJJJ 0")
assert h3.value == Value.Five
h3.jokerize()
assert h3.value == Value.Five

h4 = Hand.from_str("2JJJJ 0")
assert h4.value == Value.Four
h4.jokerize()
assert h3.value == Value.Five

h5 = Hand.from_str("2JJJA 0")
assert h5.value == Value.Three
h5.jokerize()
assert h5.value == Value.Four

h6 = Hand.from_str("234JJ 0")
assert h6.value == Value.OnePair
h6.jokerize()
assert h6.value == Value.Three


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[Hand]:
    hands = []
    for line in lines:
        hands.append(Hand.from_str(line))

    return hands


def calc1(hands: List[Hand]) -> int:
    result = 0
    sorted_hands = sorted(hands)

    for i, hand in enumerate(sorted_hands, 1):
        result += i * hand.bid
    return result


def calc2(hands: List[Hand]) -> int:
    result = 0

    for hand in hands:
        hand.jokerize()

    sorted_hands = sorted(hands)

    for i, hand in enumerate(sorted_hands, 1):
        result += i * hand.bid
    return result


if __name__ == "__main__":
    raw_data = read_data()
    hands = parse(raw_data)
    print(calc1(hands))
    print(calc2(hands))
