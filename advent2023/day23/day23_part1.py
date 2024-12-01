import sys
from typing import List, NamedTuple, Dict, Set, Tuple
from collections import defaultdict


OPPOSITE_DIR = {
    ">": "<",
    "v": "^",
    "<": ">",
    "^": "v",
}


class Coord(NamedTuple):
    x: int
    y: int


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Dict[Coord, str]:
    trails = {}

    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            trails[Coord(x, y)] = symbol

    return trails


def get_next_coords(coord: Coord) -> List[Tuple[Coord, str]]:
    new_coords = []
    for dx, dy, direction in ((-1, 0, "<"), (1, 0, ">"), (0, -1, "^"), (0, 1, "v")):
        new_coords.append((Coord(coord.x + dx, coord.y + dy), direction))
    return new_coords


def one_more_step(coord: Coord, direction: str) -> Coord:
    directions = {
        "<": (-1, 0),
        ">": (1, 0),
        "v": (0, 1),
        "^": (0, -1),
    }
    dx, dy = directions[direction]
    return Coord(coord.x + dx, coord.y + dy)


def find_all_ways(
    steps: int,
    trails: Dict[Coord, str],
    start_point: Coord,
    end_point: Coord,
    visited: Set[Coord],
    graph: List,
    first_dir="",
):
    print("------ start", start_point)
    if first_dir:
        curr_point = one_more_step(start_point, first_dir)
        visited.add(curr_point)
        steps += 1
        curr_point = one_more_step(curr_point, first_dir)
        visited.add(curr_point)
        steps += 1
    else:
        curr_point = start_point
        visited.add(start_point)

    has_moving_point = start_point

    while has_moving_point:
        print("curr", curr_point)
        has_moving_point = None

        next_steps = []
        for next_point, direction in get_next_coords(curr_point):
            if next_point not in trails or next_point in visited:
                continue

            if next_point == end_point:
                print("endpoint!")
                graph.append((start_point, end_point, steps + 1))
                return

            next_trail = trails[next_point]

            if next_trail == "#":
                continue

            if next_trail == OPPOSITE_DIR[direction]:
                continue

            steps += 1
            curr_point = next_point
            visited.add(curr_point)

            print(" next", next_point)

            if next_trail == ".":
                has_moving_point = curr_point
                break
            # print("sink!", curr_point)
            # now we've got to sink
            # make one more step and try both new directions
            #########
            # #.>.>.#
            # #.#v#.#
            # #.#.#.#
            print("curr", curr_point)
            curr_point = one_more_step(curr_point, direction)
            print(" next", curr_point)
            print("curr", curr_point)
            print("inside sink", curr_point)
            steps += 1
            print('steps', steps)
            print(sorted(visited))
            # exit()
            # visited.add(curr_point)

            graph.append((start_point, curr_point, steps))

            for next_point, direction in get_next_coords(curr_point):
                if next_point in visited:
                    continue
                next_trail = trails[next_point]
                if next_trail == "#":
                    continue

                if next_trail == OPPOSITE_DIR[direction]:
                    continue

                # print("next edge", next_point, direction, steps)
                # find_all_ways(1, trails, next_point, end_point, set(visited), graph)
                find_all_ways(0, trails, curr_point, end_point, visited, graph, first_dir=direction)

            visited.add(curr_point)
            return


# Function to find the longest path in a directed acyclic graph (DAG)
def longest_path_dag(dag, start, end):
    # Topologically sort the nodes of DAG
    topo_order = topological_sort(dag)
    # print(dag)
    # print(topo_order)
    # exit()
    # Initialize distances to all nodes as negative infinity
    # and distance to the start node as 0
    dist = {node: float("-inf") for node in topo_order}
    dist[start] = 0

    # Relax the edges in topological order
    for node in topo_order:
        for adj in dag.get(node, {}):
            if dist[adj] < dist[node] + dag[node][adj]:
                dist[adj] = dist[node] + dag[node][adj]

    return dist[end] if dist[end] != float("-inf") else None


# Function to perform Topological Sort on a DAG
def topological_sort(dag):
    visited = set()
    topo_order = []

    # Recursive function to visit nodes
    def dfs(node):
        visited.add(node)
        for neighbor in dag.get(node, {}):
            if neighbor not in visited:
                dfs(neighbor)
        topo_order.append(node)

    # Visit all nodes
    for node in dag:
        if node not in visited:
            dfs(node)

    return topo_order[::-1]  # return in reverse order for correct topological sort


def find_longest_path(trails: Dict[Coord, str]) -> int:
    start_point = next(coord for coord, value in trails.items() if coord.y == 0 and value == ".")
    max_y = max(coord.y for coord in trails)
    end_point = next(coord for coord, value in trails.items() if coord.y == max_y and value == ".")
    visited = {start_point}
    # graph = defaultdict(dict)
    graph = []

    print(start_point)
    print(end_point)

    find_all_ways(0, trails, start_point, end_point, visited, graph)
    graph = sorted(graph)
    print('graph', graph)
    exit()
    nodes = []
    dag = {}
    for node1, node2, dist in graph:
        if node1 not in nodes:
            nodes.append(node1)
        if node2 not in nodes:
            nodes.append(node2)
        num1 = nodes.index(node1)
        num2 = nodes.index(node2)

        if num1 not in dag:
            dag[num1] = {}
        dag[num1][num2] = dist

    print(dag)
    matrix = [[None for _ in range(len(nodes))] for _ in range(len(nodes))]
    for node1 in dag:
        for node2, dist in dag[node1].items():
            if matrix[node1][node2] is None:
                matrix[node1][node2] = dist
            else:
                matrix[node1][node2] = max(dist, matrix[node1][node2])
    start_node = nodes.index(start_point)
    end_node = nodes.index(end_point)
    longest_distance = longest_path_dag(dag, start_node, end_node)

    print(longest_distance)

    exit()


def calc1(trails: Dict[Coord, str]) -> int:
    result = 0
    find_longest_path(trails)
    return result


def calc2(trails: Dict[Coord, str]) -> int:
    result = 0
    return result


if __name__ == "__main__":
    raw_data = read_data()
    trails = parse(raw_data)
    print(calc1(trails))
    # print(calc2(trails))
