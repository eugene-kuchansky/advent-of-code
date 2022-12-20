import sys
from typing import List
from dataclasses import dataclass, field
import math


def read_data() -> List[int]:
    raw_data = sys.stdin.read()
    numbers = []
    numbers = [int(line) for line in raw_data.split("\n")]

    return numbers


@dataclass
class Item:
    real_value: int
    value: int = 0
    prev: "Item" = field(init=False)
    next: "Item" = field(init=False)

    def __str__(self):
        return f"[ {self.prev.value} < {self.value} > {self.next.value}]"

    def __repr__(self):
        return str(self)


def jump_forward(item, positions):
    move_forward = item.value

    new_prev_item = item.next
    for _ in range(move_forward - 1):
        new_prev_item = new_prev_item.next
    # print(new_prev_item.value)
    # print("item", item)
    # connect items around old position
    item_prev = item.prev
    item_next = item.next
    item_prev.next = item_next
    item_next.prev = item_prev

    # set item neighbors
    item.next = new_prev_item.next
    item.prev = new_prev_item

    # set pointers to item in new position
    item.next.prev = item
    new_prev_item.next = item


def jump_backward(item, positions):
    # move_back = -item.value % (len(positions) - 1)
    # if not move_back:
    #     return
    # move_back = -item.value
    move_back = -item.value

    new_next_item = item.prev
    for _ in range(move_back - 1):
        new_next_item = new_next_item.prev

    # connect items around old position
    item_prev = item.prev
    item_next = item.next
    item_prev.next = item_next
    item_next.prev = item_prev

    # set item neighbors
    item.prev = new_next_item.prev
    item.next = new_next_item

    # set pointers to item in new position
    item.prev.next = item
    new_next_item.prev = item


def move_items(positions: List[Item]):
    for item in positions:
        if item.value > 0:
            jump_forward(item, positions)

        elif item.value < 0:
            jump_backward(item, positions)


def print_list(positions: List[Item]):
    item = positions[0]
    for _ in range(len(positions)):
        print(item)
        item = item.next
    print()


def process(numbers: List[int], magic_number=1, repeat=1) -> int:
    list_len = len(numbers)
    step = list_len - 1

    positions = [Item(real_value=num) for num in numbers]
    zero_item = next(item for item in positions if item.real_value == 0)

    for i, item in enumerate(positions):
        next_num = i + 1
        if next_num == list_len:
            next_num = 0
        item.next = positions[next_num]
        item.prev = positions[i - 1]

    for item in positions:
        item.value = int(math.copysign(abs(item.real_value) * magic_number % step, item.real_value))
        if item.value > 0 and item.value > len(positions) // 2:
            item.value = -(len(positions) - 1 - item.value)
        elif item.value < 0 and -item.value > len(positions) // 2:
            item.value = len(positions) - 1 + item.value

    for _ in range(repeat):
        move_items(positions)

    result = 0
    for groove in (1000, 2000, 3000):
        move_forward = groove % len(positions)
        groove_item = zero_item
        for _ in range(move_forward):
            groove_item = groove_item.next
        result += groove_item.real_value * magic_number
    return result


def calc1(numbers: List[int]) -> int:
    return process(numbers, magic_number=1, repeat=1)


def calc2(numbers: List[int]) -> int:
    return process(numbers, magic_number=811589153, repeat=10)


if __name__ == "__main__":
    data = read_data()
    # print(calc1(data))
    print(calc2(data))
