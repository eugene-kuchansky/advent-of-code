import sys
from typing import List, Iterable, Optional, NamedTuple, Set, Tuple, Iterator, Dict


TILE_SIZE = 10

Coord = Tuple[int, int]

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


DIRECTION_SIDE = (
    (0, -1, TOP),
    (1, 0, RIGHT),
    (0, 1, BOTTOM),
    (-1, 0, LEFT),
)


OPPOSITE_SIDE = {
    TOP: BOTTOM,
    LEFT: RIGHT,
    BOTTOM: TOP,
    RIGHT: LEFT,
}

MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


class Monster(NamedTuple):
    pixels: Set[Coord]
    width: int
    height: int
    number_of_the_beast: int

    @staticmethod
    def parse(lines: List[str]) -> "Monster":
        pixels = set()
        width = len(lines[0])
        height = len(lines)
        for y, line in enumerate(lines):
            for x, value in enumerate(line):
                if value == "#":
                    pixels.add((x, y))

        return Monster(pixels, width, height, len(pixels))


class Sides(NamedTuple):
    top: int
    right: int
    bottom: int
    left: int


def get_sides(pixels: Set[Coord]) -> Sides:
    top = sum(2 << x for x in range(TILE_SIZE) if (x, 0) in pixels)
    right = sum(2 << y for y in range(TILE_SIZE) if (TILE_SIZE - 1, y) in pixels)
    bottom = sum(2 << x for x in range(TILE_SIZE) if (x, TILE_SIZE - 1) in pixels)
    left = sum(2 << y for y in range(TILE_SIZE) if (0, y) in pixels)
    return Sides(top, right, bottom, left)


def rotate_right(pixels: Set[Coord], side_size: int) -> Set[Coord]:
    return {(side_size - 1 - y, x) for (x, y) in pixels}


def flip_horizontal(pixels: Set[Coord], side_size: int) -> Set[Coord]:
    return {(side_size - 1 - x, y) for (x, y) in pixels}


def flip_vertical(pixels: Set[Coord], side_size: int) -> Set[Coord]:
    return {(x, side_size - 1 - y) for (x, y) in pixels}


class Tile(NamedTuple):
    id: int
    pixels: Set[Coord]
    sides: Sides

    @staticmethod
    def parse(raw_tile: str) -> "Tile":
        lines = raw_tile.split("\n")
        _, id_ = lines[0].strip().strip(":").split(" ")

        pixels = set()

        for y, line in enumerate(lines[1:]):
            for x, value in enumerate(line):
                if value == "#":
                    pixels.add((x, y))

        return Tile.create(int(id_), pixels)

    @staticmethod
    def create(id_: int, pixels: Set[Coord]) -> "Tile":
        sides = get_sides(pixels)
        return Tile(int(id_), pixels, sides)

    def get_sides(self) -> Sides:
        return self.sides

    def rotate_right(self) -> "Tile":
        pixels = rotate_right(self.pixels, TILE_SIZE)
        return Tile.create(self.id, pixels)

    def flip_horizontal(self) -> "Tile":
        pixels = flip_horizontal(self.pixels, TILE_SIZE)
        return Tile.create(self.id, pixels)

    def flip_vertical(self) -> "Tile":
        pixels = flip_vertical(self.pixels, TILE_SIZE)
        return Tile.create(self.id, pixels)

    def draw(self):
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                pixel = "#" if (x, y) in self.pixels else "."
                print(pixel, end="")
            print()


def read_data(stream: Iterable[str]) -> List[Tile]:
    lines = "".join([line for line in stream])
    raw_tiles = lines.split("\n\n")
    tiles = []
    for raw_tile in raw_tiles:
        tile = Tile.parse(raw_tile.strip())
        tiles.append(tile)
    return tiles


def get_tile_transformations(tile: Tile, cache: Dict) -> List[Tile]:
    if tile.id not in cache:
        cache[tile.id] = []

        for horizontal_flip in range(2):
            tile = tile.flip_horizontal()
            for vertical_flip in range(2):
                tile = tile.flip_vertical()
                for rotate_degree in range(4):
                    tile = tile.rotate_right()
                    cache[tile.id].append(tile)

    return cache[tile.id]


def with_equal_border(side: int, side_id: int, tile2: Tile, cache: Dict) -> Optional[Tile]:
    side2 = OPPOSITE_SIDE[side_id]
    for tile2 in get_tile_transformations(tile2, cache):
        if side == tile2.sides[side2]:
            return tile2
    return None


def calc1(tiles: List[Tile]) -> List[List[Tile]]:
    # tile0 = tiles[1]
    # tile0 = tile0.flip_vertical()
    # tiles[1] = tile0

    tile0 = tiles[0]

    queue = [((0, 0), tile0)]
    processed = set()
    image_coord = {(0, 0): tile0}

    cache = {}

    while queue:
        (x, y), tile1 = queue.pop()

        if tile1.id in processed:
            continue

        processed.add(tile1.id)

        for tile2 in tiles:
            if tile2.id in processed:
                continue

            for dx, dy, side_id in DIRECTION_SIDE:
                adjusted_position = (x + dx, y + dy)
                side = tile1.sides[side_id]

                if adjusted_position in image_coord:
                    continue

                adjusted_tile = with_equal_border(side, side_id, tile2, cache)

                if adjusted_tile:
                    queue.append((adjusted_position, adjusted_tile))
                    image_coord[adjusted_position] = adjusted_tile
                    break

    # ok, lets adjust coordinates as we choose random element as ground zero
    # find leftmost and bottommost and shift every point to these values
    coordinates = list(image_coord.keys())
    left = min(coordinates, key=lambda c: c[0])[0]
    bottom = min(coordinates, key=lambda c: c[1])[1]

    # transform map of tiles with coordinates to appropriate list of rows
    image_side_size = int(len(tiles) ** 0.5)
    tiles_image = [
        [image_coord[(x + left, y + bottom)] for x in range(image_side_size)] for y in range(image_side_size)
    ]

    return tiles_image


def create_gapless_image(tiles: List[List[Tile]]) -> Set[Coord]:
    actual_image = set()
    for dy, line in enumerate(tiles):
        for dx, tile in enumerate(line):
            for (x, y) in tile.pixels:
                if all([TILE_SIZE - 1 > x > 0, TILE_SIZE - 1 > y > 0]):
                    actual_image.add((x - 1 + dx * (TILE_SIZE - 2), y - 1 + dy * (TILE_SIZE - 2)))

    return actual_image


def adjust_image(image: Set[Coord], image_size: int) -> Iterator[Set[Coord]]:
    for horizontal_flip in range(2):
        image = flip_horizontal(image, image_size)
        for vertical_flip in range(2):
            image = flip_vertical(image, image_size)
            for rotate_degree in range(4):
                image = rotate_right(image, image_size)
                yield image


def find_monsters(orig_image: Set[Coord], image_size: int, monster: Monster) -> int:
    for image in adjust_image(orig_image, image_size):
        res = len(orig_image)
        monster_num = 0
        monsters = set()

        for x in range(image_size - monster.width):
            for y in range(image_size - monster.height):
                monster_image = {(x + dx, y + dy) for (dx, dy) in monster.pixels}
                if monster_image.issubset(image):
                    monsters = set.union(monsters, monster_image)
                    res -= monster.number_of_the_beast
                    monster_num += 1
        if monster_num:
            return res


def draw_image(image, image_size, monsters):
    for y in range(image_size):
        for x in range(image_size):
            pixel = "."
            if (x, y) in monsters:
                pixel = "O"
            elif (x, y) in image:
                pixel = "#"

            print(pixel, end="")
        print()


def calc2(tiles_image: List[List[Tile]]) -> int:
    image = create_gapless_image(tiles_image)

    tiles_num = len(tiles_image)
    image_size = tiles_num * TILE_SIZE - 2 * tiles_num

    monster = Monster.parse(MONSTER)
    res = find_monsters(image, image_size, monster)

    return res


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)
    result_image = calc1(initial_data)

    res1 = 1
    for i in (0, -1):
        for j in (0, -1):
            res1 *= result_image[i][j].id
    print(f"result 1: {res1}")

    res2 = calc2(result_image)
    print(f"result 2: {res2}")
