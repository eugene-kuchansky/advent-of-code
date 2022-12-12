import sys
from typing import List, Set, Tuple, Deque
from collections import deque


def read_data() -> List[List[str]]:
    return [list(line.strip()) for line in sys.stdin.readlines()]


def get_neighbors(
    row: int, col: int, height_map: List[List[str]]
) -> List[Tuple[int, int]]:
    max_rows = len(height_map)
    max_columns = len(height_map[0])
    neighbors = []
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        new_row = row + dx
        new_col = col + dy
        if new_row < 0 or new_row >= max_rows:
            continue
        if new_col < 0 or new_col >= max_columns:
            continue
        neighbors.append((new_row, new_col))
    return neighbors


def calc1(height_map: List[List[str]]) -> int:
    start_symbol = "S"
    end_symbol = "E"
    start_row = 0
    start_col = 0
    for row_num, row in enumerate(height_map):
        try:
            start_col = row.index(start_symbol)
            start_row = row_num
            break
        except ValueError:
            pass

    height_map[start_row][start_col] = "a"

    stack: Deque[Tuple[int, Tuple[int, int]], List[Tuple[int, int]]] = deque()
    path = [(start_row, start_col)]
    stack.append(path)
    visited: Set[Tuple[int, int]] = set()

    while stack:
        path = stack.popleft()
        (row_num, col_num) = path[-1]
        if (row_num, col_num) not in visited:
            if height_map[row_num][col_num] == end_symbol:
                return len(path) - 1

            visited.add((row_num, col_num))
            for new_row_num, new_col_num in get_neighbors(row_num, col_num, height_map):
                current_height = ord(height_map[row_num][col_num])

                if height_map[new_row_num][new_col_num] == end_symbol:
                    neighbor_height = ord("z")
                else:
                    neighbor_height = ord(height_map[new_row_num][new_col_num])
                if current_height < neighbor_height - 1:
                    continue
                new_path = list(path)
                new_path.append((new_row_num, new_col_num))
                stack.append(new_path)
    return 0


def calc2(height_map: List[List[str]]) -> int:
    start_symbol = "E"
    end_symbol = "a"
    start_row = 0
    start_col = 0
    for row_num, row in enumerate(height_map):
        try:
            start_col = row.index(start_symbol)
            start_row = row_num
            break
        except ValueError:
            pass
    height_map[start_row][start_col] = "z"

    stack: Deque[Tuple[int, Tuple[int, int]], List[Tuple[int, int]]] = deque()
    path = [(start_row, start_col)]
    stack.append(path)
    visited: Set[Tuple[int, int]] = set()

    while stack:
        path = stack.popleft()
        (row_num, col_num) = path[-1]
        if (row_num, col_num) not in visited:
            if height_map[row_num][col_num] == end_symbol:
                return len(path) - 1

            visited.add((row_num, col_num))
            for new_row_num, new_col_num in get_neighbors(row_num, col_num, height_map):
                current_height = ord(height_map[row_num][col_num])

                neighbor_height = ord(height_map[new_row_num][new_col_num])
                if neighbor_height < current_height - 1:
                    continue
                new_path = list(path)
                new_path.append((new_row_num, new_col_num))
                stack.append(new_path)
    return 0


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
