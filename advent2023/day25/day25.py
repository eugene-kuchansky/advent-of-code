import sys
from typing import List, Dict, Tuple
from collections import defaultdict
from dataclasses import dataclass
import random


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[Tuple[str, str]]:
    graph = []
    for line in lines:
        parent_node, others = line.split(": ")
        other_nodes = others.split(" ")
        for node in other_nodes:
            graph.append((parent_node, node))

    return graph


@dataclass
class Subset:
    # class to represent subset for union find
    # just to keep parent node and node rank
    parent: str
    rank: int


# A utility function to find set of an element i
# (uses path compression technique)
def find_parent_node(subsets: Dict[str, Subset], node: str):
    # find the chain parent (Subset) nodes of the given node
    # once the root is found we set it to the given node - this is path comprehension
    if subsets[node].parent != node:
        subsets[node].parent = find_parent_node(subsets, subsets[node].parent)

    return subsets[node].parent


def union_subsets(subsets, parent_node1, parent_node2):
    # union by rank
    # smaller rank node attached to higher rank node
    # if they are the same take first of them and increase its rank

    if subsets[parent_node1].rank < subsets[parent_node1].rank:
        parent_node1, parent_node2 = parent_node2, parent_node1
    elif subsets[parent_node1].rank == subsets[parent_node1].rank:
        subsets[parent_node1].rank += 1
    subsets[parent_node2].parent = parent_node1


def karger(graph: Dict[str, str]) -> Tuple[int, int]:
    # Karger algo https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # also we use union find and path comprehension to reduce time of search

    for _ in range(1000):
        # this is randomized algo so repeat until we find exactly 3 min cuts

        contracted_graph = graph.copy()

        # this is subset (parent) node storage
        subsets: Dict[str, Subset] = {}

        for n1, n2 in contracted_graph:
            if n1 not in subsets:
                subsets[n1] = Subset(n1, 0)

            if n2 not in subsets:
                subsets[n2] = Subset(n2, 0)

        nodes_num = len(subsets)
        while nodes_num > 2:
            # select random edge until there are only two nodes left
            i = random.randint(0, len(contracted_graph) - 1)

            node1, node2 = contracted_graph[i]
            parent_node1 = find_parent_node(subsets, node1)
            parent_node2 = find_parent_node(subsets, node2)

            if parent_node1 == parent_node2:
                # this edge connects two nodes from the same subset - edge is loop
                # remove it and go again
                del contracted_graph[i]
                continue

            # union nodes
            union_subsets(subsets, parent_node1, parent_node2)
            nodes_num -= 1

            # remove edge
            del contracted_graph[i]

        clean_graph = []
        # remove edges connecting nodes from the same loop
        for node1, node2 in contracted_graph:
            parent_node1 = find_parent_node(subsets, node1)
            parent_node2 = find_parent_node(subsets, node2)

            if parent_node1 == parent_node2:
                continue

            clean_graph.append((parent_node1, parent_node2))

        if len(clean_graph) == 3:
            # all nodes should belong to the one of the tow subsets (to one root node)
            parents = defaultdict(int)
            for subset in subsets.values():
                parent = find_parent_node(subsets, subset.parent)
                parents[parent] += 1
            num1, num2 = [value for value in parents.values()]
            return num1, num2

    raise Exception("min cut is not found")


def calc1(graph: Dict[str, str]) -> int:
    num1, num2 = karger(graph)
    result = num1 * num2

    return result


if __name__ == "__main__":
    raw_data = read_data()
    graph = parse(raw_data)
    print(calc1(graph))
