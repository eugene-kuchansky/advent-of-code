import heapq
import sys
from collections import defaultdict

COORD = tuple[int, int]


def read_data() -> tuple[dict[COORD, str], COORD, COORD]:
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
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
}


def bfs(maze: dict[COORD, str], start: COORD, end: COORD) -> tuple[int, set[COORD]]:
    queue = []
    heapq.heappush(queue, (0, start))

    visited = {}
    visited[start] = 0

    min_path = None

    while queue:
        distance, position = heapq.heappop(queue)
        if position == end:
            if not min_path:
                min_path = distance
        for dx, dy in DIRECTIONS:
            new_position = (position[0] + dx, position[1] + dy)
            new_distance = distance + 1
            if new_position in maze:
                continue
            if new_position in visited and visited[new_position] < new_distance:
                continue
            visited[new_position] = new_distance

            heapq.heappush(queue, (new_distance, new_position))
    return min_path, visited


def get_probable_steps(maze: dict[COORD, str], point: COORD, visited, steps: int) -> list[tuple[COORD, int]]:
    cheat_points = []
    for dx in range(-steps, steps + 1):
        for dy in range(-steps, steps + 1):
            if dx == dy == 0:
                continue
            add_step = abs(dx) + abs(dy)
            if add_step > steps:
                continue

            cheat_point = (point[0] + dx, point[1] + dy)
            if cheat_point not in visited or cheat_point in maze:
                continue
            if visited[cheat_point] <= (visited[point] + add_step):
                continue

            cheat_points.append((cheat_point, add_step))
    return cheat_points


def calc1(maze: dict[COORD, str], start: COORD, end: COORD) -> int:
    result = 0

    min_distance, visited = bfs(maze, start, end)
    cheats = defaultdict(int)

    for point, dist in visited.items():
        for cheat_point, steps in get_probable_steps(maze, point, visited, steps=2):
            cheat = visited[cheat_point] - visited[point] - steps
            cheats[cheat] += 1

    for cheat, count in cheats.items():
        if cheat >= 100:
            result += count
    return result


def calc2(maze: dict[COORD, str], start: COORD, end: COORD) -> int:
    result = 0

    min_distance, visited = bfs(maze, start, end)
    cheats = defaultdict(int)
    for point, dist in visited.items():
        for cheat_point, steps in get_probable_steps(maze, point, visited, steps=20):
            cheat = visited[cheat_point] - visited[point] - steps
            cheats[cheat] += 1
    for cheat, count in cheats.items():
        if cheat >= 100:
            result += count
    return result


if __name__ == "__main__":
    maze, start, end = read_data()
    print(calc1(maze, start, end))
    print(calc2(maze, start, end))
