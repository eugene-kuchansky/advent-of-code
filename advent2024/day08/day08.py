import sys
from collections import defaultdict


def read_data() -> tuple[dict[str, list[tuple[int, int]]], int, int]:
    raw_data = sys.stdin.read()

    lines = raw_data.strip().split("\n")

    width = len(lines[0])
    height = len(lines)

    antennas = defaultdict(list)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                antennas[char].append((x, y))

    return antennas, width, height


def calc1(antennas: dict[str, list[tuple[int, int]]], width: int, height: int) -> int:
    result = 0

    antinodes = set()
    for antenna, coords in antennas.items():
        for i, (x1, y1) in enumerate(coords[:-1]):
            for j, (x2, y2) in enumerate(coords[i + 1 :]):
                dx = x2 - x1
                dy = y2 - y1
                for antinode_x, antinode_y in [(x1 - dx, y1 - dy), (x2 + dx, y2 + dy)]:
                    if 0 <= antinode_x < width and 0 <= antinode_y < height:
                        antinodes.add((antinode_x, antinode_y))

    result = len(antinodes)
    return result


def calc2(antennas: dict[str, list[tuple[int, int]]], width: int, height: int):
    result = 0
    antinodes = set()
    for antenna, coords in antennas.items():
        for i, (x1, y1) in enumerate(coords[:-1]):
            for j, (x2, y2) in enumerate(coords[i + 1 :]):
                antinodes.add((x1, y1))
                antinodes.add((x2, y2))
                dx = x2 - x1
                dy = y2 - y1
                for d_sign in [1, -1]:
                    antinode_x = x1
                    antinode_y = y1
                    while 0 <= antinode_x < width and 0 <= antinode_y < height:
                        antinodes.add((antinode_x, antinode_y))
                        antinode_x += dx * d_sign
                        antinode_y += dy * d_sign

    result = len(antinodes)
    return result


if __name__ == "__main__":
    antennas, width, height = read_data()
    print(calc1(antennas, width, height))
    print(calc2(antennas, width, height))
