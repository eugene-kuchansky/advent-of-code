from typing import Tuple, Dict
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


Pixels = Dict[Tuple[int, int], str]


@dataclass
class Enhancement:
    pixels: str


@dataclass
class Image:
    enhancement: str
    pixels: Pixels
    canvas: str = "0"

    def max_x(self) -> int:
        return max(x for x, _ in self.pixels.keys()) + 1

    def max_y(self) -> int:
        return max(y for _, y in self.pixels.keys()) + 1

    def _set_new_pixel(self, source_x, source_y, max_x, max_y) -> bool:
        new_pixel = []
        for y in (source_y - 1, source_y, source_y + 1):
            for x in (source_x - 1, source_x, source_x + 1):
                if max_x > x >= 0 and max_y > y >= 0:
                    new_pixel.append(self.pixels.get((x, y), "0"))
                else:
                    new_pixel.append(self.canvas)
        ind = int("".join(new_pixel), 2)
        return self.enhancement[ind] == "#"

    def _new_canvas(self) -> str:
        if self.enhancement[0] == ".":
            # canvas does not change
            return self.canvas
        # canvas changes every time from dark to white and back
        # if now canvas is dark then take 0 enhancement pixel
        # if canvas is white take 511 (bin 111 111 111) pixel
        assert self.enhancement[511] == "."
        return "0" if self.canvas == "1" else "1"

    def enhance(self) -> "Image":
        pixels: Pixels = {}
        max_x = self.max_x()
        max_y = self.max_y()
        for y in range(max_y + 2):
            for x in range(max_x + 2):
                if self._set_new_pixel(x - 1, y - 1, max_x, max_y):
                    pixels[(x, y)] = "1"

        canvas = self._new_canvas()
        # min_x = min(x for x, _ in pixels.keys())
        # min_y = min(y for _, y in pixels.keys())
        # pixels = {(pixel[0] - min_x, pixel[1] - min_y): value for pixel, value in pixels.items()}
        return Image(self.enhancement, pixels, canvas)

    def __str__(self):
        img = [["." for x in range(self.max_x())] for y in range(self.max_y())]
        for x, y in self.pixels:
            img[y][x] = "#"
        lines = ["".join(line) for line in img]

        return "\n".join(lines)


def parse(raw: str) -> Image:
    enh_raw, image_raw = raw.split("\n\n")
    enh = enh_raw.replace("\n", "")
    assert len(enh) == 512

    pixels: Pixels = {}
    for y, line in enumerate(image_raw.splitlines()):
        for x, pixel in enumerate(line):
            if pixel == "#":
                pixels[(x, y)] = "1"
    return Image(enh, pixels)


def calc(image: Image, steps=2) -> int:
    for _ in range(steps):
        image = image.enhance()
    # print(image)
    return len(image.pixels)


RAW = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

assert calc(parse(RAW)) == 35
# assert calc(parse(RAW), 50) == 3351

if __name__ == "__main__":
    raw = read_data()
    print(calc(parse(raw)))
    print(calc(parse(raw), 50))
