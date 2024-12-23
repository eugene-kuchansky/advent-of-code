import sys
from collections import deque


def read_data() -> list[tuple[int, int]]:
    raw_data = sys.stdin.read()
    bytes_list = []
    for line in raw_data.strip().split("\n"):
        b1, b2 = line.split(",")
        bytes_list.append((int(b1), int(b2)))

    return bytes_list


DIRECTIONS = (
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, 0),
)


def dfs(
    maze: dict[tuple[int, int], str],
    queue: deque,
    end: tuple[int, int],
    visited: set[tuple[int, int]],
    max_size: int,
) -> tuple[bool, set[tuple[int, int]], list[tuple[int, int]]]:
    while queue:
        distance, position, path = queue.popleft()

        if position == end:
            return True, visited, path

        for dx, dy in DIRECTIONS:
            new_position = (position[0] + dx, position[1] + dy)
            if not (0 <= new_position[0] < max_size) or not (0 <= new_position[1] < max_size):
                continue

            if new_position in maze:
                continue
            if new_position in visited:
                continue
            visited.add(new_position)

            queue.append((distance + 1, new_position, path + [new_position]))

    return False, visited, []


def calc1(bytes_list: list[tuple[int, int]]) -> int:
    result = 0

    if len(bytes_list) > 25:
        max_size = 71
        max_length = 1024
    else:
        max_size = 7
        max_length = 12

    maze = {(i, j): "#" for i, j in bytes_list[:max_length]}
    start = (0, 0)
    end = (max_size - 1, max_size - 1)
    queue = deque()
    queue.append((0, start, []))
    visited = {start}
    _, _, path = dfs(maze, queue, end, visited, max_size)

    result = len(path)

    return result


def calc2(bytes_list: list[tuple[int, int]]) -> str:
    result = 0

    if len(bytes_list) > 25:
        max_size = 71
    else:
        max_size = 7

    maze = {(i, j): "#" for i, j in bytes_list}
    start = (0, 0)
    end = (max_size - 1, max_size - 1)

    queue = deque()
    queue.append((0, start, []))

    visited = {start}

    last_byte = None
    is_found, visited, path = dfs(maze, queue, end, visited, max_size)

    while not is_found:
        last_byte = bytes_list.pop()
        del maze[last_byte]

        for dx, dy in DIRECTIONS:
            new_position = (last_byte[0] + dx, last_byte[1] + dy)
            if not (0 <= new_position[0] < max_size) or not (0 <= new_position[1] < max_size):
                continue
            if new_position in maze:
                continue
            if new_position in visited:
                queue.append((0, new_position, []))

        is_found, visited, path = dfs(maze, queue, end, visited, max_size)

    result = f"{last_byte[0]},{last_byte[1]}"

    return result


if __name__ == "__main__":
    bytes_list = read_data()
    print(calc1(bytes_list))
    print(calc2(bytes_list))
