from collections import namedtuple
from string import ascii_lowercase as KEYS, ascii_uppercase as DOORS
from collections import deque


Position = namedtuple("Position", "x y")

MOVES = ((0, 1), (0, -1), (1, 0), (-1, 0))

WALL = "#"
ENTRANCE = "@"
CACHE = {}


def read_data(file_name):
    with open(file_name) as f:
        raw_data = f.read()

    x = 0
    y = 0
    board = {}
    keys = {}
    entrances = []
    doors = {}

    for i in raw_data:
        if i == "\n":
            x = 0
            y += 1
        else:
            position = Position(x, y)
            board[position] = i
            x += 1
            if i == ENTRANCE:
                entrances.append(position)
            elif i in KEYS:
                keys[i] = position
            elif i in DOORS:
                doors[i] = position
    return board, keys, doors, entrances


def shortest_path(pos1, board):
    q = deque()
    required_keys_for_keys = {}
    required_keys = []
    steps_to_keys = {}

    steps = {}
    step = 0

    q.append((pos1, required_keys, step))

    while q:
        pos, required_keys, step = q.popleft()
        steps[pos] = step

        required_keys = list(required_keys)

        if board[pos] in DOORS:
            required_keys.append(board[pos])
        elif board[pos] in KEYS and pos != pos1:
            steps_to_keys[board[pos]] = step
            required_keys_for_keys[board[pos]] = set(_.lower() for _ in required_keys)

        for (x, y) in MOVES:
            new_pos = Position(pos.x + x, pos.y + y)
            if new_pos not in board or new_pos in steps or board[new_pos] == WALL:
                continue
            q.append((new_pos, required_keys, step + 1))
    return steps_to_keys, required_keys_for_keys


def get_available_keys(place, collected_keys, maps):
    required_keys_for_keys = maps[place]["required_keys_for_keys"]
    available_keys = []
    for k, required_keys in required_keys_for_keys.items():
        if k in collected_keys:
            continue
        if required_keys.issubset(collected_keys):
            available_keys.append(k)
    return available_keys


def part1():
    board, keys, doors, entrances = read_data("input_data/18_1.txt")
    steps_to_keys, required_keys_for_keys = shortest_path(entrances[0], board)
    maps = {
        ENTRANCE: {
            "steps_to_keys": steps_to_keys,
            "required_keys_for_keys": required_keys_for_keys,
        }
    }
    for k, pos in keys.items():
        steps_to_keys, required_keys_for_keys = shortest_path(pos, board)
        maps[k] = {
            "steps_to_keys": steps_to_keys,
            "required_keys_for_keys": required_keys_for_keys,
        }

    min_steps = find_min_steps(
        places=(ENTRANCE, ),
        collected_keys=frozenset(),
        maps=maps,
        all_keys_len=len(keys.keys()),
    )
    print(min_steps)


def find_min_steps(places, collected_keys, maps, all_keys_len):
    if len(collected_keys) == all_keys_len:
        return 0

    cache_key = ''.join(sorted(places)) + " " + ''.join(sorted(collected_keys))

    if cache_key in CACHE:
        return CACHE[cache_key]

    results = []

    for place in places:
        available_keys = get_available_keys(place, collected_keys, maps)

        if not available_keys:
            continue
        steps_to_keys = maps[place]["steps_to_keys"]
        for k in available_keys:
            results.append((steps_to_keys[k], k, place))
    results = sorted(results, key=lambda x: (x[0], x[1]))

    min_steps = None

    for steps_to_keys_k, k, place in results:
        if min_steps is not None and min_steps <= steps_to_keys_k:
            continue
        new_places = tuple(k if p == place else p for p in places)
        curr_steps = find_min_steps(new_places, collected_keys.union(k), maps, all_keys_len) + steps_to_keys_k

        if min_steps is None:
            min_steps = curr_steps
        elif min_steps > curr_steps:
            min_steps = curr_steps

    CACHE[cache_key] = min_steps
    return min_steps


def part2():
    CACHE.clear()

    board, keys, doors, entrances = read_data("input_data/18_2.txt")
    maps = {}
    for i, entrance in enumerate(entrances):
        num = str(i)
        board[entrance] = num
        steps_to_keys, required_keys_for_keys = shortest_path(entrance, board)
        maps[num] = {
            "steps_to_keys": steps_to_keys,
            "required_keys_for_keys": required_keys_for_keys,
        }

        available_keys = list(steps_to_keys.keys())

        for k, pos in keys.items():
            if k not in available_keys:
                continue
            steps_to_keys, required_keys_for_keys = shortest_path(pos, board)
            maps[k] = {
                "steps_to_keys": steps_to_keys,
                "required_keys_for_keys": required_keys_for_keys,
            }

    min_steps = find_min_steps(
        places=("0", "1", "2", "3"),
        collected_keys=frozenset(),
        maps=maps,
        all_keys_len=len(keys.keys())
    )
    print(min_steps)


if __name__ == "__main__":
    #part1()
    part2()
