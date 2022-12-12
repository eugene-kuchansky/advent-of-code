from typing import Optional, List, Union, Tuple
from dataclasses import dataclass
import json
from copy import deepcopy
import math


@dataclass
class Node:
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    value: Optional[int] = None
    is_leaf: bool = False
    parent: Optional["Node"] = None

    def __repr__(self):
        if self.is_leaf:
            return f"{self.value}"
        else:
            return f"[{self.left},{self.right}]"


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_tree(line: str) -> Node:
    data = json.loads(line)
    return create_node(data)


def create_node(element: Union[List, int], parent: Optional[Node] = None) -> Node:
    if isinstance(element, list):
        left, right = element
        node = Node(parent=parent)
        node.left = create_node(left, node)
        node.right = create_node(right, node)
        return node
    elif isinstance(element, int):
        return Node(value=element, is_leaf=True, parent=parent)


def parse(raw: str) -> List[Node]:
    return [parse_tree(line) for line in raw.splitlines()]


def add_nodes(node1: Node, node2: Node) -> Node:
    new_node = Node(left=deepcopy(node1), right=deepcopy(node2))
    new_node.left.parent = new_node
    new_node.right.parent = new_node
    return new_node


# should be rewritten to return left and right to top node to add
# instead of using parent to search nearest left and right
def explode(node: Optional[Node], level=0):
    if node is None:
        raise ValueError("wtf", node)

    if node.is_leaf:
        return False

    if level >= 4:
        new_node = Node(value=0, is_leaf=True, parent=node.parent)

        if node.parent.left is node:
            node.parent.left = new_node
        else:
            node.parent.right = new_node

        add_left_up(new_node.parent, new_node, node.left.value)
        add_right_up(new_node.parent, new_node, node.right.value)

        return True

    if explode(node.left, level=level + 1):
        return True

    return explode(node.right, level=level + 1)


def add_right_down(node, value):
    if node is None:
        return
    if node.is_leaf:
        node.value += value
        return
    add_right_down(node.right, value)


def add_left_down(node, value):
    if node is None:
        return
    if node.is_leaf:
        node.value += value
        return
    add_left_down(node.left, value)


def add_right_up(node, from_node, value):
    if node is None:
        return
    if node.is_leaf:
        node.value += value
        return
    if node.right is from_node:
        add_right_up(node.parent, node, value)
        return
    add_left_down(node.right, value)


def add_left_up(node, from_node, value):
    if node is None:
        return
    if node.is_leaf:
        node.value += value
        return
    if node.left is from_node:
        add_left_up(node.parent, node, value)
        return
    add_right_down(node.left, value)


def div_number(n: int) -> Tuple[int, int]:
    n1 = n // 2
    n2 = math.ceil(n / 2)
    # if n % 2:
    #     n2 += 1
    return n1, n2


def split(node: Optional[Node]) -> bool:
    if node is None:
        raise ValueError("wtf", node)

    if node.is_leaf:
        if node.value < 10:
            return False

        left_value, right_value = div_number(node.value)
        node.is_leaf = False
        node.left = Node(value=left_value, is_leaf=True, parent=node)
        node.right = Node(value=right_value, is_leaf=True, parent=node)

        return True

    if split(node.left):
        return True

    return split(node.right)


def reduce(node: Node):
    while True:
        if explode(node):
            continue

        if not split(node):
            break


def magnitude(node: Node) -> int:
    if node.is_leaf:
        return node.value
    return 3 * magnitude(node.left) + 2 * magnitude(node.right)


def sum_nodes(numbers: List[Node]) -> Node:
    number = numbers[0]
    for other_number in numbers[1:]:
        number = add_nodes(number, other_number)
        reduce(number)
    return number


def calc(numbers: List[Node]) -> int:
    node = sum_nodes(numbers)
    return magnitude(node)


def calc2(numbers: List[Node]) -> int:
    max_mag = -1
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            sum_node = sum_nodes([numbers[i], numbers[j]])
            mag1 = magnitude(sum_node)

            sum_node = sum_nodes([numbers[j], numbers[i]])
            mag2 = magnitude(sum_node)

            max_mag = max(max_mag, mag1, mag2)
    return max_mag


RAW1 = "[[1,2],3]"
node1 = parse_tree(RAW1)
assert str(node1) == RAW1

RAW2 = "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"
node2 = parse_tree(RAW2)
assert str(node2) == RAW2

RAW3 = "[[[[[9,8],1],2],3],4]"
node3 = parse_tree(RAW3)
assert str(node3) == RAW3
explode(node3)
assert str(node3) == "[[[[0,9],2],3],4]"

RAW4 = "[7,[6,[5,[4,[3,2]]]]]"
node4 = parse_tree(RAW4)
assert str(node4) == RAW4
explode(node4)
assert str(node4) == "[7,[6,[5,[7,0]]]]"


RAW5 = "[[6,[5,[4,[3,2]]]],1]"
node5 = parse_tree(RAW5)
assert str(node5) == RAW5
explode(node5)
assert str(node5) == "[[6,[5,[7,0]]],3]"

RAW6 = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
node6 = parse_tree(RAW6)
assert str(node6) == RAW6
reduce(node6)
assert str(node6) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"


RAW7 = "[[[[4,3],4],4],[7,[[8,4],9]]]"
node7 = parse_tree(RAW7)

RAW8 = "[1,1]"
node8 = parse_tree(RAW8)
node9 = add_nodes(node7, node8)

assert str(node9) == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
reduce(node9)
assert str(node9) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

RAW_LIST1 = """[1,1]
[2,2]
[3,3]
[4,4]"""

assert str(sum_nodes(parse(RAW_LIST1))) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"

RAW_LIST2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""

assert str(sum_nodes(parse(RAW_LIST2))) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"


RAW_LIST3 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""

assert str(sum_nodes(parse(RAW_LIST3))) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

RAW_LIST4 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""

assert str(sum_nodes((parse(RAW_LIST4)))) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

RAW_LIST5 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

sum_node5 = sum_nodes((parse(RAW_LIST5)))
assert str(sum_node5) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
assert magnitude(sum_node5) == 4140

assert calc2(parse(RAW_LIST5)) == 3993


if __name__ == "__main__":
    raw = read_data()
    print(calc(parse(raw)))
    print(calc2(parse(raw)))
