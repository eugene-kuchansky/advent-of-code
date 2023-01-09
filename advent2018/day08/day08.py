import sys
from typing import Tuple, List, Dict, Set, Optional
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    children: List["Node"]
    metadata: List[int]
    len: int
    value: Optional[int] = None

    def calc(self) -> int:
        if self.value is not None:
            return self.value

        self.value = 0
        if not self.children:
            self.value = sum(self.metadata)
            return self.value

        for num in self.metadata:
            if num > 0 and num <= len(self.children):
                self.value += self.children[num - 1].calc()

        return self.value

    def sum_metadata(self) -> int:
        return sum(self.metadata) + sum(sum_metadata(child) for child in self.children)


def read_data() -> List[int]:
    raw_data = sys.stdin.read()
    return [int(num) for num in raw_data.split(" ")]


def create_node(numbers) -> Node:
    children_num = numbers[0]
    metadata_len = numbers[1]

    children = []
    start = 2
    for _ in range(children_num):
        child = create_node(numbers[start:])
        start += child.len
        children.append(child)

    metadata_start = start
    metadata_end = metadata_start + metadata_len
    node = Node(
        children,
        metadata=numbers[metadata_start:metadata_end],
        len=metadata_end,
    )
    return node


def sum_metadata(node: Node) -> int:
    return sum(node.metadata) + sum(sum_metadata(child) for child in node.children)


def calc1(numbers: List[int]) -> int:
    root = create_node(numbers)
    return root.sum_metadata()


def calc2(numbers: List[int]) -> int:
    root = create_node(numbers)
    return root.calc()


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
