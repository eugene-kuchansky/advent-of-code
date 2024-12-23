import sys
from collections import defaultdict, deque
from heapq import heappop, heappush


def read_data() -> tuple[dict[tuple[int, int], str], tuple[int, int], tuple[int, int]]:
    raw_data = sys.stdin.read()
    start = (0, 0)
    end = (0, 0)
    maze = {}
    for y, line in enumerate(raw_data.strip().split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                maze[(x, y)] = char
            elif char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)

    return maze, start, end


DIRECTIONS = {
    "north": (0, -1),
    "east": (1, 0),
    "south": (0, 1),
    "west": (-1, 0),
}

TURNS = {
    "right": {
        "north": "east",
        "east": "south",
        "south": "west",
        "west": "north",
    },
    "left": {
        "north": "west",
        "east": "north",
        "south": "east",
        "west": "south",
    },
}


def bfs(
    maze: dict[tuple[int, int], str], start: tuple[int, int], end: tuple[int, int]
) -> tuple[int, list[tuple[int, int]]]:
    queue = [
        (0, start, "east", [(start, "east", 0)]),
    ]

    visited = set(start)

    while queue:
        distance, position, direction, path = heappop(queue)
        if position == end:
            return distance, path

        for new_direction, (dx, dy) in DIRECTIONS.items():
            new_position = (position[0] + dx, position[1] + dy)
            if new_position in maze:
                continue
            if new_position in visited:
                continue
            visited.add(new_position)
            if new_direction == direction:
                new_distance = distance + 1
            else:
                new_distance = distance + 1000 + 1
            heappush(
                queue, (new_distance, new_position, new_direction, path + [(new_position, new_direction, new_distance)])
            )


# Backtrack to find all shortest paths
def reconstruct_paths(state, start, parents):
    pos, _ = state
    if state[0] == start:
        return [[pos]]
    all_paths = []
    for parent in parents[state]:
        for path in reconstruct_paths(parent, start, parents):
            all_paths.append(path + [pos])
    return all_paths


def bfs_all(
    maze: dict[tuple[int, int], str], start: tuple[int, int], end: tuple[int, int]
) -> tuple[int, list[tuple[int, int]]]:
    queue = deque()
    queue.append((0, start, "east"))

    visited = {
        (start, "east"): 0,
    }

    shortest_distance = None
    parents = defaultdict(list)

    while queue:
        distance, position, direction = queue.popleft()

        if position == end:
            if not shortest_distance or distance < shortest_distance:
                shortest_distance = distance
            continue

        all_directions = [
            (direction, DIRECTIONS[direction], 1),
            (TURNS["right"][direction], DIRECTIONS[TURNS["right"][direction]], 1001),
            (TURNS["left"][direction], DIRECTIONS[TURNS["left"][direction]], 1001),
        ]
        for new_direction, (dx, dy), cost in all_directions:
            new_position = (position[0] + dx, position[1] + dy)
            if new_position in maze:
                continue

            new_distance = distance + cost

            if shortest_distance and new_distance > shortest_distance:
                continue

            if (new_position, new_direction) not in visited or visited[(new_position, new_direction)] > new_distance:
                visited[(new_position, new_direction)] = new_distance
                parents[(new_position, new_direction)] = [(position, direction)]

                queue.append((new_distance, new_position, new_direction))
            elif visited[(new_position, new_direction)] == new_distance:
                parents[(new_position, new_direction)].append((position, direction))

    end_states = [(pos, orientation) for (pos, orientation) in visited if pos == end]
    shortest_paths = []

    for state in end_states:
        if visited[state] == shortest_distance:
            paths = reconstruct_paths(state, start, parents)
            for path in paths:
                shortest_paths.append(path)
    return shortest_paths


def calc1(
    maze: dict[tuple[int, int], str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    result = 0
    result, _ = bfs(maze, start, end)
    return result


def calc2(
    maze: dict[tuple[int, int], str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    result = 0

    paths = bfs_all(maze, start, end)
    positions = set()
    for path in paths:
        for position in path:
            positions.add(position)
    result = len(positions)

    return result


if __name__ == "__main__":
    maze, start, end = read_data()
    print(calc1(maze, start, end))
    print(calc2(maze, start, end))
