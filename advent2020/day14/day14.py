import sys
from typing import Iterable, List, NamedTuple, Iterator


class Memory:
    def __init__(self):
        self._memory = {}

    def write(self, addr: int, value: int):
        self._memory[addr] = value

    def sum(self):
        return sum(self._memory.values())


class Value(NamedTuple):
    addr: int
    value: int

    @staticmethod
    def parse(item: str) -> "Value":
        mem, value = item.split(" = ")
        addr = mem.replace("mem[", "").replace("]", "")
        return Value(int(addr), int(value))


class Operation(NamedTuple):
    mask: str
    operations: List[Value]

    @staticmethod
    def parse(item: str, values: List[Value]) -> "Operation":
        _, mask = item.split(" = ")
        return Operation(mask, values)


def read_data(stream: Iterable[str]) -> List[Operation]:
    operations = []
    values = []
    mask = ""
    for line in stream:
        item = line.strip()
        if item.startswith("mask"):
            if mask:
                operation = Operation.parse(mask, values)
                operations.append(operation)
                values = []
            mask = item
        else:
            values.append(Value.parse(item))

    operation = Operation.parse(mask, values)
    operations.append(operation)

    return operations


def apply_mask(mask: str, value: int) -> int:
    for i, bit in enumerate(reversed(mask)):
        sub_mask = 1 << i
        if bit == "1":
            value = value | sub_mask
        elif bit == "0":
            value = value & ~sub_mask
    return value


def apply_mask2(mask: str, value: int) -> str:
    bin_value = list(bin(value)[2:].rjust(len(mask), "0"))
    for i, bit in enumerate(mask):
        if bit != "0":
            bin_value[i] = bit
    return "".join(bin_value)


def calc1(operations: List[Operation]) -> int:
    mem = Memory()
    for operation in operations:
        for value in operation.operations:
            mem.write(value.addr, apply_mask(operation.mask, value.value))

    return mem.sum()


def apply_mem_mask(mask: str) -> Iterator[int]:
    count_x = mask.count("X")
    for i in range(2 ** count_x):
        new_mask = mask
        while i:
            bit = i % 2
            new_mask = new_mask.replace("X", str(bit), 1)
            i = i >> 1
        new_mask = new_mask.replace("X", "0")
        yield int(new_mask, 2)


def calc2(operations: List[Operation]) -> int:
    mem = Memory()
    for operation in operations:
        for value in operation.operations:
            mem_mask = apply_mask2(operation.mask, value.addr)
            for addr in apply_mem_mask(mem_mask):
                mem.write(addr, value.value)

    return mem.sum()


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
