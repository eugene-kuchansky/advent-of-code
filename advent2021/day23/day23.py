from typing import List, Dict, Union, Tuple, Set
from dataclasses import dataclass
import string
import heapq


BURROW = """#############
#qw.e.r.t.yu#
###A#B#C#D###
  #E#F#G#H#
  #########
"""

BURROW2 = """#############
#qw.e.r.t.yu#
###A#B#C#D###
  #E#F#G#H#
  #I#J#K#L#
  #M#N#O#P#
  #########"""


ROOMS = (
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
)

ROOMS2 = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P")

AVAILABLE_POINTS = ("q", "w", "e", "r", "t", "y", "u")

ROOMS_TYPES = {
    "a": ["E", "A"],
    "b": ["F", "B"],
    "c": ["G", "C"],
    "d": ["H", "D"],
}

ROOMS_TYPES2 = {
    "a": ["M", "I", "E", "A"],
    "b": ["N", "J", "F", "B"],
    "c": ["O", "K", "G", "C"],
    "d": ["P", "L", "H", "D"],
}

ENERGIES = {
    "a": 1,
    "b": 10,
    "c": 100,
    "d": 1000,
}


def find_all_routes(burrow: str, rooms_types: Dict[str, List[str]]):
    burrow_schema = [list(line) for line in burrow.splitlines()]

    room_to_type: Dict[str, str] = {}
    for a_type, rooms_chars in rooms_types.items():
        for room_char in rooms_chars:
            room_to_type[room_char] = a_type

    from_rooms: Dict[str, Dict[str, Dict[str, Union[List[str], int]]]] = {}
    for start_point_char in room_to_type:
        from_rooms[start_point_char] = {}
        routes = find_routes(start_point_char, burrow_schema, target=string.ascii_lowercase)
        for route, info in routes.items():
            if room_to_type[start_point_char] == room_to_type.get(route):
                continue
            from_rooms[start_point_char][route] = info

    to_rooms: Dict[str, Dict[str, Dict[str, Union[List[str], int]]]] = {}
    points = tuple(room_to_type.keys()) + AVAILABLE_POINTS
    for start_point_char in points:
        to_rooms[start_point_char] = {}
        routes = find_routes(start_point_char, burrow_schema, target=string.ascii_uppercase)
        for route, info in routes.items():
            if room_to_type.get(start_point_char) == room_to_type.get(route):
                continue
            to_rooms[start_point_char][route] = info
    from_rooms = {r: from_rooms[r] for r in sorted(from_rooms)}
    to_rooms = {r: to_rooms[r] for r in sorted(to_rooms)}
    return from_rooms, to_rooms


def get_start_pos(start_point_char: str, burrow: List[List[str]]) -> Tuple[int, int]:
    for i, row in enumerate(burrow):
        for j, col in enumerate(row):
            if col == start_point_char:
                return (i, j)
    raise Exception(f"{start_point_char} not found")


def find_routes(
    start_point_char: str, burrow: List[List[str]], target: str
) -> Dict[str, Dict[str, Union[List[str], int]]]:
    row, col = get_start_pos(start_point_char, burrow)

    path: List[str] = []
    length: int = 0
    q: List[Tuple[Tuple[int, int], List[str], int]] = [((row, col), path, length)]
    visited = set()
    paths: Dict[str, Dict[str, Union[List[str], int]]] = {}
    while q:
        (row, col), path, length = q.pop()
        visited.add((row, col))
        point = burrow[row][col]

        if point in string.ascii_letters:
            path.append(point)

        if point in target:
            paths[point] = {"path": path[1:-1], "length": length}

        for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_row = row + d_row
            new_col = col + d_col
            new_point = burrow[new_row][new_col]
            if new_point == "#" or (new_row, new_col) in visited:
                continue
            q.append(((new_row, new_col), path[:], length + 1))

    return paths


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


@dataclass(order=True)
class Amphipod:
    type: str
    places: List[str]
    rooms: List[str]
    energy: int
    target: int = 0


def parse(lines: List[str], rooms_types) -> List[Amphipod]:
    amphipods_list = [
        Amphipod(type=a_type, places=[], rooms=rooms_types[a_type], energy=ENERGIES[a_type]) for a_type in "abcd"
    ]
    amphipods: Dict[str, Amphipod] = {}

    for amphipod in amphipods_list:
        amphipods[amphipod.type] = amphipod

    rooms_layer_ind = 0
    for layer_ind in range(len(lines) - 2, 1, -1):
        room_layer = lines[layer_ind].strip(" #")

        rooms_list = {
            0: rooms_types["a"][rooms_layer_ind],
            1: rooms_types["b"][rooms_layer_ind],
            2: rooms_types["c"][rooms_layer_ind],
            3: rooms_types["d"][rooms_layer_ind],
        }

        for room_num, amphipod_type in enumerate(room_layer.split("#")):
            amphipod_type = amphipod_type.lower()
            room = rooms_list[room_num]

            a = amphipods[amphipod_type]
            if room == a.rooms[a.target] and a.target == rooms_layer_ind:
                a.target += 1
            else:
                a.places.append(room)

        rooms_layer_ind += 1

    return amphipods_list


def is_organized(amphipods: List[Amphipod]) -> bool:
    for amphipod in amphipods:
        if amphipod.places:
            return False
    return True


def goto(from_place: str, to_place: str, occupied: Set[str], paths) -> int:
    if to_place in occupied:
        return 0
    if from_place == to_place:
        return 0
    path = paths[from_place][to_place]["path"]
    for place in path:
        if place in occupied:
            return 0
    return paths[from_place][to_place]["length"]


def get_occupied(amphipods: List[Amphipod], rooms_num):
    # rooms_num = len(amphipods[0].rooms)
    occupied_places = set()
    for amphipod in amphipods:
        len_places = len(amphipod.places)
        places = amphipod.places + amphipod.rooms[: rooms_num - len_places]
        for place in places:
            occupied_places.add(place)
    return occupied_places


def available_steps(amphipods: List[Amphipod], from_rooms, to_rooms, rooms_num):
    occupied_places = get_occupied(amphipods, rooms_num)

    moves = []

    for i, amphipod in enumerate(amphipods):
        if not amphipod.places:
            continue

        target_room = amphipod.rooms[amphipod.target]

        for from_place in amphipod.places:
            step_num = goto(from_place, target_room, occupied_places, to_rooms)
            if step_num:

                updated_amphipods = amphipods[:]
                a = updated_amphipods[i]
                updated_amphipods[i] = Amphipod(a.type, a.places[:], a.rooms[:], a.energy, a.target)
                updated_amphipod = updated_amphipods[i]

                updated_amphipod.places = [
                    other_place for other_place in updated_amphipod.places if other_place != from_place
                ]
                updated_amphipod.target += 1
                moves.append((updated_amphipods, step_num * amphipod.energy))
                continue

            if from_place not in string.ascii_uppercase:
                continue

            for available_place in AVAILABLE_POINTS:
                step_num = goto(from_place, available_place, occupied_places, from_rooms)
                if step_num:
                    updated_amphipods = amphipods[:]
                    a = updated_amphipods[i]
                    updated_amphipods[i] = Amphipod(a.type, a.places[:], a.rooms[:], a.energy, a.target)
                    updated_amphipod = updated_amphipods[i]

                    updated_amphipod.places = [
                        available_place if place == from_place else place for place in updated_amphipod.places
                    ]
                    moves.append((updated_amphipods, step_num * amphipod.energy))
    return moves


def amphipods_to_key(amphipods: List[Amphipod], energy: int, rooms_num: int):
    positions = []
    for amphipod in amphipods:
        len_places = len(amphipod.places)
        places = sorted(amphipod.places + amphipod.rooms[: rooms_num - len_places])
        positions.extend(places)
    positions.append(str(energy))
    return tuple(positions)


def print_borrow(amphipods, burrow, rooms):
    rooms_num = len(amphipods[0].rooms)
    for i, amphipod in enumerate(amphipods):
        len_places = len(amphipod.places)
        places = sorted(amphipod.places + amphipod.rooms[: rooms_num - len_places])

        for place in places:
            burrow = burrow.replace(place, str(i))

    for point in AVAILABLE_POINTS:
        burrow = burrow.replace(point, ".")
    for point in rooms:
        burrow = burrow.replace(point, ".")
    for i, amphipod in enumerate(amphipods):
        burrow = burrow.replace(str(i), amphipod.type.upper())
    print(burrow)


class Wrapper:
    def __init__(self, amphipods, energy):
        self.amphipods = amphipods
        self.energy = energy

    def __lt__(self, other):
        return self.energy < other.energy

    def __eq__(self, other):
        return self.energy == other.energy


def calc(amphipods: List[Amphipod], from_rooms, to_rooms, rooms_num: int) -> int:
    # from_rooms, to_rooms = find_all_routes(BURROW, ROOMS_TYPES)
    q: List = []
    energy = 0

    visited = set()
    while True:
        visited.add(amphipods_to_key(amphipods, energy, rooms_num))

        for updated_amphipods, step_energy in available_steps(amphipods, from_rooms, to_rooms, rooms_num):
            updated_energy = energy + step_energy
            if amphipods_to_key(updated_amphipods, updated_energy, rooms_num) in visited:
                continue
            heapq.heappush(q, (updated_energy, updated_amphipods))

        energy, amphipods = heapq.heappop(q)
        # energy, amphipods = wrapped.energy, wrapped.amphipods
        if is_organized(amphipods):
            return energy
    return 0


# def calc2(amphipods: List[Amphipod]) -> int:

#     # from_rooms, to_rooms = find_all_routes(BURROW2, ROOMS_TYPES2)
#     q: List[Wrapper] = []
#     energy = 0

#     visited = set()
#     while True:
#         k = amphipods_to_key(amphipods, energy, 4)
#         visited.add(k)

#         for updated_amphipods, step_energy in available_steps(amphipods, from_rooms, to_rooms, 4):
#             updated_energy = energy + step_energy

#             if amphipods_to_key(updated_amphipods, updated_energy, 4) in visited:
#                 continue
#             heapq.heappush(q, Wrapper(updated_amphipods, updated_energy))

#         wrapped = heapq.heappop(q)
#         energy, amphipods = wrapped.energy, wrapped.amphipods
#         if is_organized(amphipods):
#             return energy
#     return 0


RAW = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

LINES = RAW.splitlines()

AMPHIPODS = parse(LINES, ROOMS_TYPES)
assert AMPHIPODS[0].target == 1
assert AMPHIPODS[0].places == ["H"]
assert AMPHIPODS[1].target == 0
assert AMPHIPODS[1].places == ["A", "C"]

FROM_ROOMS, TO_ROOMS = find_all_routes(BURROW, ROOMS_TYPES)
assert calc(AMPHIPODS, FROM_ROOMS, TO_ROOMS, rooms_num=2) == 12521

EXTRA_LINES = [
    "  #D#C#B#A#",
    "  #D#B#A#C#",
]

LINES2 = LINES[:3] + EXTRA_LINES + LINES[3:]

AMPHIPODS2 = parse(LINES2, ROOMS_TYPES2)
FROM_ROOMS2, TO_ROOMS2 = find_all_routes(BURROW2, ROOMS_TYPES2)

if __name__ == "__main__":
    raw = read_data()
    lines = raw.splitlines()

    from_rooms, to_rooms = find_all_routes(BURROW, ROOMS_TYPES)
    print(calc(parse(lines, ROOMS_TYPES), from_rooms, to_rooms, rooms_num=2))

    lines2 = lines[:3] + EXTRA_LINES + lines[3:]
    from_rooms2, to_rooms2 = find_all_routes(BURROW2, ROOMS_TYPES2)
    print(calc(parse(lines2, ROOMS_TYPES2), from_rooms2, to_rooms2, rooms_num=4))
