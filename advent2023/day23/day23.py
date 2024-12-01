import sys
from typing import List, NamedTuple, Dict, Set, Tuple
from collections import defaultdict
from functools import cache

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
    visited_nodes: Set[Tuple[Coord, Coord]],
    graph: List,
    first_dir="",
):
    # print(visited_nodes)
    # print("------ start", start_point)
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

    while True:
        # print("curr", curr_point)

        valid_next = []

        for next_point, direction in get_next_coords(curr_point):
            # print("next_point, direction", next_point, direction)
            if next_point not in trails or next_point in visited:
                # print("next_point not in trails", next_point not in trails)
                # print("next_point in visited", next_point in visited)
                continue

            next_trail = trails[next_point]

            if next_trail == "#":
                continue

            valid_next.append((next_point, direction))
        # print(valid_next)

        if not valid_next:
            return

        if len(valid_next) == 1:
            next_point, direction = valid_next[0]

            if next_point == end_point:
                # print("endpoint!")
                visited_nodes.add((start_point, end_point))
                graph.append((start_point, end_point, steps + 1))
                return

            # print(" next", next_point)
            steps += 1
            curr_point = next_point
            visited.add(curr_point)
            continue

            # # if next_trail == ".":
            # #     has_moving_point = curr_point
            # #     break
            # # print("sink!", curr_point)
            # # now we've got to sink
            # # make one more step and try both new directions
            # #########
            # # #.>.>.#
            # # #.#v#.#
            # # #.#.#.#
            # curr_point = one_more_step(curr_point, direction)
            # print("inside sink", curr_point)
            # steps += 1
            # # visited.add(curr_point)

        # print("found node", curr_point)
        if (start_point, curr_point) in visited_nodes:
            return
        # if (curr_point, start_point) in visited_nodes:
        #     return

        visited_nodes.add((start_point, curr_point))

        visited.remove(curr_point)
        graph.append((start_point, curr_point, steps))

        # print("inside sink", curr_point)
        # print("steps", steps)
        # print(sorted(visited))
        # exit()
        for next_point, direction in valid_next:
            if trails[next_point] == OPPOSITE_DIR[direction]:
                continue

            # if next_point in visited:
            #     continue
            # next_trail = trails[next_point]
            # if next_trail == "#":
            #     continue

            # if next_trail == OPPOSITE_DIR[direction]:
            #     continue

            # print("next edge", next_point, direction, steps)
            # find_all_ways(1, trails, next_point, end_point, set(visited), graph)
            # find_all_ways(0, trails, curr_point, end_point, visited, graph, first_dir=direction)
            find_all_ways(0, trails, curr_point, end_point, set(), visited_nodes, graph, first_dir=direction)

        visited.add(curr_point)
        # print(" reached bootom")
        return


# Function to find the longest path in a directed acyclic graph (DAG)
def longest_path_dag(dag, start, end):
    # Topologically sort the nodes of DAG
    topo_order = topological_sort(dag)
    # print(dag)
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
    visited_nodes = set()
    # graph = defaultdict(dict)
    graph = []

    print(start_point)
    print(end_point)

    find_all_ways(0, trails, start_point, end_point, visited, visited_nodes, graph)
    graph = sorted(graph)
    print("graph")
    for g in graph:
        print(g)
    print()
    # res = longest_path(graph, start_point, end_point)
    # print(res)

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
    print("nodes", nodes)
    print(len(nodes))
    matrix = [[None for _ in range(len(nodes))] for _ in range(len(nodes))]
    for node1 in dag:
        for node2, dist in dag[node1].items():
            if matrix[node1][node2] is None:
                matrix[node1][node2] = dist
            else:
                matrix[node1][node2] = max(dist, matrix[node1][node2])
    start_node = nodes.index(start_point)
    end_node = nodes.index(end_point)
    for row in matrix:
        for i in row:
            if i is None:
                print(None, end=" ")
            else:
                print(f"{i:4}", end=" ")
        print()
    exit()
    # print(start_node, end_node)
    longest_distance = longest_path_dag(dag, start_node, end_node)

    print(longest_distance)

    exit()


def dfs(visited, current_node, end, adj_list, memo):
    # If reached the end, return 0 as there's no further path
    if current_node == end:
        return 0

    # If the problem is already solved, return the result
    if (visited, current_node) in memo:
        return memo[(visited, current_node)]

    length = float("-inf")  # Initialize as negative infinity
    for neighbor, weight in adj_list[current_node]:
        if neighbor not in visited:
            # Calculate the longest path via neighbor
            length = max(length, dfs(visited.union({neighbor}), neighbor, end, adj_list, memo) + weight)

    # Save and return the longest length found
    memo[(visited, current_node)] = length
    return length


def longest_path(graph, start, end):
    # Convert graph to adjacency list with weights
    adj_list = defaultdict(list)
    for u, v, w in graph:
        adj_list[u].append((v, w))
    print()
    for a in adj_list:
        print(a, adj_list[a])

    # Memoization table, where key is a tuple (visited, last_node)
    memo = {}

    # DFS function to explore all paths and find the longest one

    # Start DFS from the start node with an empty path
    longest_length = dfs(frozenset([start]), start, end, adj_list, memo)
    return longest_length if longest_length != float("-inf") else 0  # Return 0 if no path found


# def longest_path(graph, start, end, n):
#     # Convert graph to adjacency matrix or list for easy access
#     # Assuming graph[i][j] is the weight of edge i->j, -1 if no direct edge

#     # Initialize DP array: -inf for all values initially except the start node
#     DP = [[float("-inf") for _ in range(1 << n)] for _ in range(n)]
#     DP[start][1 << start] = 0  # Distance to start node with only it visited is 0

#     # Iterate over all states of visited nodes
#     for visited in range(1 << n):
#         for u in range(n):
#             # Skip if u isn't visited yet in this state
#             if not visited & (1 << u):
#                 continue

#             # Try to extend the path to all possible next nodes v
#             for v in range(n):
#                 if graph[u][v] != -1 and not visited & (1 << v):  # If edge exists and v is not yet visited
#                     # Update DP for new state with v visited and ending at v
#                     new_visited = visited | (1 << v)
#                     DP[v][new_visited] = max(DP[v][new_visited], DP[u][visited] + graph[u][v])

#     # Answer is the maximum value in DP for end node with all nodes visited
#     # As we need at least the start and end nodes to be visited, we start with them in the visited mask
#     best_path = max(DP[end][visited] for visited in range(1 << n) if visited & (1 << end))
#     return best_path if best_path != float("-inf") else 0


def calc1(trails: Dict[Coord, str]) -> int:
    result = 0
    find_longest_path(trails)
    return result


def calc2(trails: Dict[Coord, str]) -> int:
    result = 0
    for coord, trail in trails.items():
        if trail in OPPOSITE_DIR:
            trails[coord] = "."
    find_longest_path(trails)
    return result


if __name__ == "__main__":
    raw_data = read_data()
    trails = parse(raw_data)
    # print(calc1(trails))
    print(calc2(trails))
