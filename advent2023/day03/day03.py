import sys
from typing import List, Dict, Tuple
import re
import itertools


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse_numbers(line: str) -> Dict[int, str]:
    pattern = r"\d+"
    matches = re.finditer(pattern, line)

    result = {}

    for group in matches:
        number = group.group()
        start_position = group.start()
        result[start_position] = number

    return result


def parse_symbols(line: str) -> Dict[int, str]:
    pattern = r"[^0-9.]"
    matches = re.finditer(pattern, line)

    result = {}

    for group in matches:
        symbol = group.group()
        start_position = group.start()
        result[start_position] = symbol

    return result


def parse(lines: List[str]) -> Tuple[List[Dict[int, str]], List[Dict[int, str]]]:
    symbols = []
    numbers = []
    for line in lines:
        numbers.append(parse_numbers(line))
        symbols.append(parse_symbols(line))
    return symbols, numbers


def get_coords_around(line_num, start_pos, num) -> List[Tuple[int, int]]:
    top = [(line_num - 1, start_pos + i - 1) for i in range(len(num) + 2)]

    bottom = [(line_num + 1, start_pos + i - 1) for i in range(len(num) + 2)]
    around = [(line_num, start_pos - 1), (line_num, start_pos + len(num))]

    return list(itertools.chain(top, bottom, around))


def is_symbol_adjacent(symbols: List[Dict[int, str]], coords: List[Tuple[int, int]]) -> bool:
    for line_num, pos in coords:
        if line_num < 0 or line_num == len(symbols):
            continue

        if symbols[line_num].get(pos):
            return True

    return False


def symbol_adjacent_nums(
    symbols: List[Dict[int, List[str]]], coords: List[Tuple[int, int]], num: str
) -> List[Dict[int, List[str]]]:
    for line_num, pos in coords:
        if line_num < 0 or line_num == len(symbols):
            continue

        if pos in symbols[line_num]:
            symbols[line_num][pos].append(num)

    return symbols


def calc1(symbols: List[Dict[int, str]], numbers: List[Dict[int, str]]) -> int:
    result = 0
    for line_num, line_numbers in enumerate(numbers):
        for start_pos, num in line_numbers.items():
            coords = get_coords_around(line_num, start_pos, num)
            if is_symbol_adjacent(symbols, coords):
                result += int(num)

    return result


def calc2(symbols: List[Dict[int, str]], numbers: List[Dict[int, str]]) -> int:
    result = 0
    gear_symbols_num = [{pos: [] for pos, symbol in line.items() if symbol == "*"} for line in symbols]

    for line_num, line_numbers in enumerate(numbers):
        for start_pos, num in line_numbers.items():
            coords = get_coords_around(line_num, start_pos, num)
            gear_symbols_num = symbol_adjacent_nums(gear_symbols_num, coords, num)
    for line_gears in gear_symbols_num:
        for adjacent_nums in line_gears.values():
            if len(adjacent_nums) == 2:
                result += int(adjacent_nums[0]) * int(adjacent_nums[1])
    return result


if __name__ == "__main__":
    raw_data = read_data()
    symbols, numbers = parse(raw_data)
    print(calc1(symbols, numbers))
    print(calc2(symbols, numbers))
