from typing import List, Set, Dict, FrozenSet
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


DIGITS = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}

# we know the unique lengths segments of 1, 7, 4, 8
LEN_TO_DIGIT = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}


RAW = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


RAW2 = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""


@dataclass
class Display:
    digits: List[Set]
    message: List[Set]

    def decode(self) -> int:
        digit_to_num = self._decode_mapping()
        return self._parse_message(digit_to_num)

    def _decode_mapping(self) -> Dict[FrozenSet, int]:
        digit_to_num: Dict[FrozenSet, int] = {}
        num_to_digit: List[Set] = [set()] * 10

        for digit in self.digits:
            decoded_digit = LEN_TO_DIGIT.get(len(digit))
            # 1 4 7 8
            if decoded_digit is not None:
                digit_to_num[frozenset(digit)] = decoded_digit
                num_to_digit[decoded_digit] = digit

        for digit in self.digits:
            if len(digit) == 6:
                # 0 6 9
                if digit.issuperset(num_to_digit[4]):
                    # 9 contains all the segments of 4
                    decoded_digit = 9
                elif digit.issuperset(num_to_digit[1]):
                    # 0 contains  all the segments of 1
                    decoded_digit = 0
                else:
                    decoded_digit = 6
                digit_to_num[frozenset(digit)] = decoded_digit
                num_to_digit[decoded_digit] = digit

        for digit in self.digits:
            if len(digit) == 5:
                # 2 3 5
                if digit.issuperset(num_to_digit[1]):
                    # 3 contains  all the segments of 1
                    decoded_digit = 3
                elif num_to_digit[6].issuperset(digit):
                    # 5 contains  all the segments of 6
                    decoded_digit = 5
                else:
                    decoded_digit = 2
                digit_to_num[frozenset(digit)] = decoded_digit
                num_to_digit[decoded_digit] = digit

        return digit_to_num

    def _parse_message(self, digit_to_num: Dict[FrozenSet, int]) -> int:
        numbers = [digit_to_num[frozenset(digit)] for digit in self.message]
        return int("".join([str(number) for number in numbers]))


def parse(raw: str) -> List[Display]:
    displays = []
    for line in raw.split("\n"):
        raw_digits, raw_message = line.split(" | ")
        digits = [set(_) for _ in raw_digits.split()]
        message = [set(_) for _ in raw_message.split()]
        displays.append(Display(digits, message))
    return displays


def calc(displays: List[Display]) -> int:
    search_nums_count = 0

    # lenths of (1, 4, 7, 8)
    known_lengths = set(LEN_TO_DIGIT.keys())

    for display in displays:
        for encoded_digit in display.message:
            if len(encoded_digit) in known_lengths:
                search_nums_count += 1
    return search_nums_count


def calc2(displays: List[Display]) -> int:
    return sum([display.decode() for display in displays])


assert calc(parse(RAW)) == 26
assert calc2(parse(RAW)) == 61229
assert calc2(parse(RAW2)) == 5353


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data)))
    print(calc2(parse(raw_data)))
