import sys
from typing import Iterable, Tuple, List, Dict, Set


def get_cups(numbers: List[int]) -> Dict[int, int]:
    pointers = {cup: numbers[i + 1] for i, cup in enumerate(numbers[:-1])}
    pointers[numbers[-1]] = numbers[0]
    return pointers


def read_data(stream: Iterable[str]) -> Tuple[Dict[int, int], List[int]]:
    raw = [line.strip() for line in stream][0]
    numbers = [int(number) for number in raw]
    pointers = get_cups(numbers)
    return pointers, numbers


def get_destination_cup(current_cup: int, pickup_values: Set[int], min_number: int, max_number: int) -> int:
    destination_cup = current_cup
    while True:
        destination_cup -= 1
        if destination_cup < min_number:
            destination_cup = max_number
        if destination_cup not in pickup_values:
            break
    return destination_cup


def make_move(current_cup: int, pointers: Dict[int, int], min_number: int, max_number: int) -> int:
    # get pointers to first and last pickups
    first_pickup = pointers[current_cup]
    second_pickup = pointers[first_pickup]
    last_pickup = pointers[second_pickup]

    # remove pickups from circle
    pointers[current_cup] = pointers[last_pickup]

    # get destination value which is not in pickups
    pickup_values = {first_pickup, second_pickup, last_pickup}
    destination_cup = get_destination_cup(current_cup, pickup_values, min_number, max_number)

    # insert pickups next to destination
    pointers[last_pickup] = pointers[destination_cup]
    pointers[destination_cup] = first_pickup

    return pointers[current_cup]


def print_cups(pointers: Dict[int, int], current_cup: int):
    first = list(pointers.values())[0]
    cup = first
    while pointers[cup] != first:
        if current_cup == cup:
            print(f"({cup})", end=" ")
        else:
            print(cup, end=" ")
        cup = pointers[cup]
    if current_cup == cup:
        print(f"({cup})", end=" ")
    else:
        print(cup, end=" ")
    print()


def get_result1(pointers: Dict[int, int]) -> str:
    values = []
    cup = pointers[1]
    while cup != 1:
        values.append(cup)
        cup = pointers[cup]
    return "".join([str(value) for value in values])


def get_result2(pointers: Dict[int, int]) -> int:
    next_cup1 = pointers[1]
    next_cup2 = pointers[next_cup1]
    return next_cup1 * next_cup2


def calc1(pointers: Dict[int, int], cup: int) -> str:
    numbers = list(pointers.keys())
    min_number = min(numbers)
    max_number = max(numbers)
    # print(1, end=": ")
    print_cups(pointers, cup)
    for i in range(100):
        # print(f"-- move {i + 1} --")
        # print("cups: ", end="")
        print_cups(pointers, cup)
        cup = make_move(cup, pointers, min_number, max_number)
        # print()

    print_cups(pointers, cup)
    return get_result1(pointers)


def calc2(init_numbers: List[int]) -> int:
    total_numbers = 1000000
    max_number = max(init_numbers)
    other_numbers = [i for i in range(max_number+1, total_numbers+1)]
    numbers = init_numbers + other_numbers

    pointers = get_cups(numbers)

    min_number = min(init_numbers)
    max_number = total_numbers
    cup = init_numbers[0]
    for i in range(10000000):
        cup = make_move(cup, pointers, min_number, max_number)
    return get_result2(pointers)


if __name__ == "__main__":
    initial_pointers, initial_numbers = read_data(sys.stdin)
    # res1 = calc1(initial_pointers, initial_numbers[0])
    # print(f"result 1: {res1}")

    res2 = calc2(initial_numbers)
    print(f"result 2: {res2}")
