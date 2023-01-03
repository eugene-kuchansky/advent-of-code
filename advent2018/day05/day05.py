import sys
from typing import Tuple, Optional
from dataclasses import dataclass
import string


@dataclass
class Item:
    value: str
    lower_value: str
    prev: Optional["Item"]
    next: Optional["Item"]


def read_data() -> Tuple[Item, int]:
    raw_data = sys.stdin.read()
    return raw_data


def create_linked_list(letters: str) -> Item:
    prev = None
    head = None
    for letter in letters:
        item = Item(letter, letter.lower(), prev=prev, next=None)

        if head is None:
            head = item
        else:
            prev.next = item

        prev = item
    return head


def get_reduced_list(current: Item) -> str:
    while current is not None and current.next is not None:
        if not (current.lower_value == current.next.lower_value and current.value != current.next.value):
            current = current.next
            continue

        if current.next.next is None:
            current = current.prev
            current.next = None
            continue

        if current.prev is None:
            current = current.next.next
            current.prev = None
            continue

        current = current.prev
        current.next = current.next.next.next
        current.next.prev = current
    while current.prev is not None:
        current = current.prev
    reduced_list = []
    while current is not None:
        reduced_list.append(current.value)
        current = current.next
    return reduced_list


def calc1(letters: str) -> int:
    head = create_linked_list(letters)
    reduced_list = get_reduced_list(head)
    return len(reduced_list)


def calc2(letters: str) -> int:
    head = create_linked_list(letters)
    reduced_list = get_reduced_list(head)
    shortest_polymer = len(letters)
    for remove_letter in string.ascii_lowercase:
        without_letter_list = [
            letter for letter in reduced_list if letter not in (remove_letter, remove_letter.upper())
        ]
        head = create_linked_list("".join(without_letter_list))
        reduced_list_without_letter = get_reduced_list(head)
        if len(reduced_list_without_letter) < shortest_polymer:
            shortest_polymer = len(reduced_list_without_letter)
    return shortest_polymer


if __name__ == "__main__":
    raw_data = read_data()
    # print(calc1(raw_data))
    print(calc2(raw_data))
