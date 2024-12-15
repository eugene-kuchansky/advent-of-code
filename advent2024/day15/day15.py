import sys
from typing import Callable


def read_data() -> tuple[dict[tuple[int, int], str], dict[tuple[int, int], str], tuple[int, int], list[str]]:
    raw_data = sys.stdin.read()
    warehouse = {}
    boxes = {}
    moves = []
    robot_position = (0, 0)
    warehouse_lines, moves_lines = raw_data.strip().split("\n\n")
    for y, line in enumerate(warehouse_lines.split("\n")):
        for x, char in enumerate(line):
            if char == "O":
                boxes[(x, y)] = char
            elif char == "#":
                warehouse[(x, y)] = char
            elif char == "@":
                robot_position = (x, y)

    for move_line in moves_lines.splitlines():
        moves.extend(list(move_line.strip()))
    return warehouse, boxes, robot_position, moves


def display_warehouse(
    warehouse: dict[tuple[int, int], str], boxes: dict[tuple[int, int], str], robot_position: tuple[int, int]
):
    max_x = max(x for x, _ in warehouse)
    max_y = max(y for _, y in warehouse)

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if (x, y) == robot_position:
                print("@", end="")
            elif (x, y) in boxes:
                print(boxes[(x, y)], end="")
            elif (x, y) in warehouse:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


DIRECTIONS = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


def move_boxes(
    boxes: dict[tuple[int, int], str], boxes_to_move: dict[tuple[int, int], str], dx: int, dy: int
) -> dict[tuple[int, int], str]:
    new_boxes = {}
    for (x, y), box in boxes.items():
        if (x, y) in boxes_to_move:
            new_boxes[(x + dx, y + dy)] = boxes_to_move[(x, y)]
        else:
            new_boxes[(x, y)] = box
    return new_boxes


def move_robot(
    warehouse: dict[tuple[int, int], str],
    boxes: dict[tuple[int, int], str],
    robot_position: tuple[int, int],
    move: str,
    can_move_boxes: Callable[
        [dict[tuple[int, int], str], dict[tuple[int, int], str], tuple[int, int], int, int],
        tuple[bool, dict[tuple[int, int], str]],
    ],
) -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    (dx, dy) = DIRECTIONS[move]

    next_position = (robot_position[0] + dx, robot_position[1] + dy)

    if next_position in warehouse:
        new_robot_position = robot_position
    elif next_position in boxes:
        can_move, boxes_to_move = can_move_boxes(warehouse, boxes, next_position, dx, dy)
        if can_move:
            new_robot_position = next_position
            boxes = move_boxes(boxes, boxes_to_move, dx, dy)
        else:
            new_robot_position = robot_position
    else:
        new_robot_position = next_position
    return boxes, new_robot_position


def can_move_boxes1(
    warehouse: dict[tuple[int, int], str],
    boxes: dict[tuple[int, int], str],
    box_position: tuple[int, int],
    dx: int,
    dy: int,
) -> tuple[bool, dict[tuple[int, int], str]]:
    next_move = (box_position[0] + dx, box_position[1] + dy)
    boxes_to_move = {}
    if next_move in warehouse:
        can_move = False
    elif next_move in boxes:
        can_move, boxes_to_move = can_move_boxes1(warehouse, boxes, next_move, dx, dy)
    else:
        can_move = True
    if can_move:
        boxes_to_move[box_position] = boxes[box_position]
    return can_move, boxes_to_move


def can_move_boxes2(
    warehouse: dict[tuple[int, int], str],
    boxes: dict[tuple[int, int], str],
    box_position: tuple[int, int],
    dx: int,
    dy: int,
) -> tuple[bool, dict[tuple[int, int], str]]:
    next_move = (box_position[0] + dx, box_position[1] + dy)
    boxes_to_move = {}
    can_move = True

    check = [(next_move, box_position)]
    if dx == 0:
        # add box part to check only for vertical moves
        if boxes[box_position] == "[":
            # print("it's left part")
            box_part_position = (box_position[0] + 1, box_position[1])
        else:
            # print("it's right part")
            box_part_position = (box_position[0] - 1, box_position[1])
        next_move_part_position = (box_part_position[0] + dx, box_part_position[1] + dy)
        check.append((next_move_part_position, box_part_position))

    for next_move, box_position in check:
        if next_move in warehouse:
            can_move = False
            break
        elif next_move in boxes:
            can_move_partial, boxes_to_move_partial = can_move_boxes2(warehouse, boxes, next_move, dx, dy)
            if can_move_partial:
                boxes_to_move_partial[box_position] = boxes[box_position]
                boxes_to_move.update(boxes_to_move_partial)
            else:
                can_move = False
                break
        else:
            boxes_to_move[box_position] = boxes[box_position]
    return can_move, boxes_to_move


def calc1(
    warehouse: dict[tuple[int, int], str],
    boxes: dict[tuple[int, int], str],
    robot_position: tuple[int, int],
    moves: list[str],
) -> int:
    result = 0
    display_warehouse(warehouse, boxes, robot_position)

    for move in moves:
        boxes, robot_position = move_robot(warehouse, boxes, robot_position, move, can_move_boxes1)

    display_warehouse(warehouse, boxes, robot_position)
    for box_x, box_y in boxes:
        result += box_y * 100 + box_x
    return result


def expand_warehouse(warehouse: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    new_warehouse = {}
    for x, y in warehouse:
        new_warehouse[(x * 2, y)] = warehouse[(x, y)]
        new_warehouse[(x * 2 + 1, y)] = warehouse[(x, y)]

    return new_warehouse


def expand_boxes(boxes: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    new_boxes = {}
    for x, y in boxes:
        new_boxes[(x * 2, y)] = "["
        new_boxes[(x * 2 + 1, y)] = "]"
    return new_boxes


def calc2(
    warehouse: dict[tuple[int, int], str],
    boxes: dict[tuple[int, int], str],
    robot_position: tuple[int, int],
    moves: list[str],
) -> int:
    result = 0
    warehouse = expand_warehouse(warehouse)
    boxes = expand_boxes(boxes)
    robot_position = (robot_position[0] * 2, robot_position[1])
    display_warehouse(warehouse, boxes, robot_position)

    for move in moves:
        boxes, robot_position = move_robot(warehouse, boxes, robot_position, move, can_move_boxes2)

    display_warehouse(warehouse, boxes, robot_position)
    for (box_x, box_y), box_char in boxes.items():
        if box_char == "[":
            result += box_y * 100 + box_x
    return result


if __name__ == "__main__":
    warehouse, boxes, robot_position, moves = read_data()
    print(calc1(warehouse.copy(), boxes.copy(), robot_position, moves))
    print(calc2(warehouse.copy(), boxes.copy(), robot_position, moves))
