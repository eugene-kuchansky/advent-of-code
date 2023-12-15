import sys
from typing import List, NamedTuple


class Lens(NamedTuple):
    label: str
    focal: int


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[str]:
    sequence = [_ for _ in lines[0].split(",")]

    return sequence


def hashing(step: str) -> int:
    value = 0
    for char in step:
        value = ((value + ord(char)) * 17) % 256

    return value


def calc1(sequence: List[str]) -> int:
    result = 0
    for step in sequence:
        result += hashing(step)
    return result


def add_to_box(box: List[Lens], label: str, focal: int) -> List[Lens]:
    new_lens = Lens(label, focal)
    for ind, lens in enumerate(box):
        if lens.label == new_lens.label:
            box[ind] = new_lens
            return box
    box.append(new_lens)
    return box


def rm_from_box(box: List[Lens], label: str) -> List[Lens]:
    return [lens for lens in box if lens.label != label]


def calc2(sequence: List[str]) -> int:
    boxes: List[List[Lens]] = [[] for _ in range(256)]

    for step in sequence:
        if "-" in step:
            label = step[:-1]
            focal = None
        else:
            label, focal = step.split("=")
            focal = int(focal)

        box_ind = hashing(label)
        box = boxes[box_ind]

        if focal is not None:
            box = add_to_box(box, label, focal)
        else:
            box = rm_from_box(box, label)
        boxes[box_ind] = box

    result = 0
    for box_ind, box in enumerate(boxes):
        for slot_ind, lens in enumerate(box):
            result += (box_ind + 1) * (slot_ind + 1) * lens.focal

    return result


if __name__ == "__main__":
    raw_data = read_data()
    sequence = parse(raw_data)
    print(calc1(sequence))
    print(calc2(sequence))
