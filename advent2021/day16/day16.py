from typing import List
from dataclasses import dataclass, field
import math


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


@dataclass
class Packet:
    raw_bits: str
    version: int = 0
    type_id: int = 0
    header_size: int = 6
    size: int = 6
    sub_packets: List["Packet"] = field(default_factory=list)

    def __post_init__(self):
        self.version = int(self.raw_bits[0:3], 2)
        self.type_id = int(self.raw_bits[3:6], 2)
        self.parse()

    def __len__(self) -> int:
        return self.size

    def parse(self):
        pass

    def calculate(self):
        pass

    def sum_versions(self) -> int:
        return sum(sub_packet.sum_versions() for sub_packet in self.sub_packets) + self.version


@dataclass
class Literal(Packet):
    value: int = 0
    chunk_size: int = 5

    def parse(self):
        start = self.header_size
        chunks = []
        while True:
            chunks.append(self.raw_bits[start + 1 : start + 5])
            if self._is_last_chunk(start):
                break
            start += self.chunk_size
        self.value = int("".join(chunks), 2)

        self.size += len(chunks) * self.chunk_size

    def _is_last_chunk(self, start) -> bool:
        return self.raw_bits[start] == "0"

    def calculate(self):
        return self.value


@dataclass
class OperatorSub(Packet):
    header_size: int = 7
    size: int = 7

    def calculate(self) -> int:
        if self.type_id == 0:
            return sum(packet.calculate() for packet in self.sub_packets)
        if self.type_id == 1:
            return math.prod(packet.calculate() for packet in self.sub_packets)
        if self.type_id == 2:
            return min(packet.calculate() for packet in self.sub_packets)
        if self.type_id == 3:
            return max(packet.calculate() for packet in self.sub_packets)

        if self.type_id == 5:
            return 1 if self.sub_packets[0].calculate() > self.sub_packets[1].calculate() else 0
        if self.type_id == 6:
            return 1 if self.sub_packets[0].calculate() < self.sub_packets[1].calculate() else 0
        if self.type_id == 7:
            return 1 if self.sub_packets[0].calculate() == self.sub_packets[1].calculate() else 0

        raise RuntimeError(f"Unknown type id = {self.type_id}")


@dataclass
class OperatorSubLen(OperatorSub):
    len_size: int = 15  # size of length of bits of sub-packets

    def parse(self):
        sub_packets_len = int(self.raw_bits[self.header_size : self.header_size + self.len_size], 2)
        self.size += self.len_size

        start = self.size
        self.size += sub_packets_len

        while start < self.size:
            sub_packet = get_packet(self.raw_bits[start:])
            self.sub_packets.append(sub_packet)
            start += len(sub_packet)


@dataclass
class OperatorSubNum(OperatorSub):
    len_size: int = 11  # size of number of sub-packets

    def parse(self):
        sub_packets_number = int(self.raw_bits[self.header_size : self.header_size + self.len_size], 2)
        self.size += self.len_size

        for _ in range(sub_packets_number):
            sub_packet = get_packet(self.raw_bits[self.size :])
            self.sub_packets.append(sub_packet)
            self.size += len(sub_packet)


def parse(raw: str) -> str:
    return "".join([bin(int(_, 16))[2:].zfill(4) for _ in list(raw)])


def get_packet(raw_bits: str) -> Packet:
    if raw_bits[3:6] == "100":
        return Literal(raw_bits)
    if raw_bits[6] == "0":
        return OperatorSubLen(raw_bits)
    else:
        return OperatorSubNum(raw_bits)


def calc(raw_bits: str) -> int:
    packet = get_packet(raw_bits)
    return packet.sum_versions()


def calc2(raw_bits: str) -> int:
    packet = get_packet(raw_bits)
    return packet.calculate()


raw_bits1 = parse("D2FE28")
assert raw_bits1 == "110100101111111000101000"
packet1 = get_packet(raw_bits1)
assert isinstance(packet1, Literal)
assert len(packet1) == 21
assert packet1.value == 2021


raw_bits2 = parse("38006F45291200")
assert raw_bits2 == "00111000000000000110111101000101001010010001001000000000"
packet2 = get_packet(raw_bits2)
assert isinstance(packet2, OperatorSubLen)
assert len(packet2) == 49
assert len(packet2.sub_packets) == 2

raw_bits3 = parse("EE00D40C823060")
assert raw_bits3 == "11101110000000001101010000001100100000100011000001100000"
packet3 = get_packet(raw_bits3)
assert isinstance(packet3, OperatorSubNum)
assert len(packet3) == 51
assert len(packet3.sub_packets) == 3


assert calc(parse("8A004A801A8002F478")) == 16
assert calc(parse("620080001611562C8802118E34")) == 12
assert calc(parse("C0015000016115A2E0802F182340")) == 23
assert calc(parse("A0016C880162017C3686B18A3D4780")) == 31


assert calc2(parse("C200B40A82")) == 3
assert calc2(parse("04005AC33890")) == 54
assert calc2(parse("880086C3E88112")) == 7
assert calc2(parse("CE00C43D881120")) == 9
assert calc2(parse("D8005AC2A8F0")) == 1
assert calc2(parse("F600BC2D8F")) == 0
assert calc2(parse("9C005AC2F8F0")) == 0
assert calc2(parse("9C0141080250320F1802104A08")) == 1


if __name__ == "__main__":
    raw = read_data()
    print(calc(parse(raw)))
    print(calc2(parse(raw)))
