import sys
from typing import List, Dict, Tuple
from dataclasses import dataclass
from itertools import cycle
from sympy.ntheory.modular import solve_congruence


@dataclass
class Node:
    name: str
    left: str
    right: str


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Tuple[List[str], Dict[str, Node]]:
    path = list(lines[0])

    nodes = {}
    for line in lines[1:]:
        name, other_nodes = line.split(" = ")
        left, right = other_nodes[1:-1].split(", ")
        nodes[name] = Node(name, left, right)

    return path, nodes


def calc1(path: List[str], nodes: Dict[str, Node]) -> int:
    result = 0
    current_name = "AAA"
    iter_path = cycle(path)

    while current_name != "ZZZ":
        current_node = nodes[current_name]
        turn = next(iter_path)
        current_name = current_node.left if turn == "L" else current_node.right
        result += 1

    return result


def get_circle(node_name: str, path: List[str], nodes: Dict[str, Node]) -> Tuple[int, int]:
    # find step where we visit once again end node on the same path element

    step = 0
    current_name = node_name
    iter_path = cycle(path)

    visited_steps = {}
    visited_reminders = {}

    end_nodes = {node_name for node_name in nodes if node_name[-1] == "Z"}

    while True:
        # the whole calculation can be simplified as it appears that only one end node is the result
        # and it creates cycle from the start
        current_node = nodes[current_name]
        turn = next(iter_path)
        current_name = current_node.left if turn == "L" else current_node.right
        step += 1

        if current_name not in end_nodes:
            continue

        reminder = step % len(path)

        if current_name not in visited_steps:
            visited_reminders[current_name] = [reminder]
            visited_steps[current_name] = [step]
            continue

        if reminder in visited_reminders[current_name]:
            ind = visited_reminders[current_name].index(reminder)
            return visited_steps[current_name][ind], step - visited_steps[current_name][ind]

        visited_reminders[current_name].append(reminder)
        visited_steps[current_name].append(step)


def calc2(path: List[str], nodes: Dict[str, Node]) -> int:
    params = []

    for node_name in nodes:
        if node_name[-1] != "A":
            continue
        start, repeat = get_circle(node_name, path, nodes)
        params.append((start, repeat))

    # Chinese Remainder Theorem is used here
    # did it many times so just skip this part
    _, result = solve_congruence(*params)

    return result


if __name__ == "__main__":
    raw_data = read_data()
    path, nodes = parse(raw_data)
    print(calc1(path, nodes))
    print(calc2(path, nodes))
