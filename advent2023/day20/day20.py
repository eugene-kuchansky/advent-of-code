import sys
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field
from collections import deque
import math

BROADCASTER = "broadcaster"

LOW = 0
HIGH = 1


@dataclass
class Device:
    name: str
    signal: int = LOW

    def send_signal(self, signal: int, from_device: "Device") -> Optional[int]:
        self.signal = signal
        return self.signal


@dataclass
class Dummy(Device):
    name: str
    signal: int = LOW

    def send_signal(self, signal: int, from_device: "Device") -> Optional[int]:
        self.signal = signal
        return None


@dataclass
class Broadcaster(Device):
    def send_signal(self, signal, from_device: "Device") -> Optional[int]:
        self.signal = signal
        return self.signal


@dataclass
class Flipflop(Device):
    def send_signal(self, signal: int, from_device: "Device") -> Optional[int]:
        if signal == HIGH:
            return self.signal
        self.signal = int(not (self.signal))
        return self.signal


@dataclass
class Conjunction(Device):
    register: Dict[str, int] = field(default_factory=dict)

    def register_source(self, device_name: str):
        self.register[device_name] = LOW

    def send_signal(self, signal: int, from_device: Device) -> Optional[int]:
        self.register[from_device] = signal
        # all_signals = list(self.register.values())
        if any(s == LOW for s in self.register.values()):
            self.signal = HIGH
        else:
            self.signal = LOW
        return self.signal


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Tuple[Dict[str, List[str]], Dict[str, Device]]:
    network = {}
    devices = {}

    classes = {
        "b": Broadcaster,
        "%": Flipflop,
        "&": Conjunction,
    }

    for line in lines:
        device, connections = line.split(" -> ")
        device_class = classes[device[0]]
        if device[0] == BROADCASTER[0]:
            name = BROADCASTER
        else:
            name = device[1:]
        connected_devices = connections.split(", ")
        network[name] = connected_devices
        devices[name] = device_class(name=name)

    for source_name, connected_devices in network.items():
        for name in connected_devices:
            if name not in devices:
                devices[name] = Dummy(name=name)

    for name, device in devices.items():
        if isinstance(device, Conjunction):
            for source_name, connected_devices in network.items():
                if name in connected_devices:
                    device.register_source(source_name)

    return network, devices


def click(network: Dict[str, List[str]], devices: Dict[str, Device]):
    pulses = {
        HIGH: 0,
        LOW: 1,
    }

    q = deque()
    for name in network[BROADCASTER]:
        q.append((LOW, name, BROADCASTER))

    while q:
        signal, name, from_name = q.popleft()

        pulses[signal] += 1

        if name not in network:
            continue

        device = devices[name]

        if signal == HIGH and isinstance(device, Flipflop):
            continue

        new_signal = device.send_signal(signal, from_name)

        for next_name in network[name]:
            q.append((new_signal, next_name, name))

    return pulses


def find_cycle(network: Dict[str, List[str]], devices: Dict[str, Device]):
    for name, connected in network.items():
        if "rx" in connected:
            final_module = name
            break

    cycles = {name: 0 for name in devices[final_module].register}

    for i in range(10000):
        q = deque()
        for name in network[BROADCASTER]:
            q.append((LOW, name, BROADCASTER))

        while q:
            signal, name, from_name = q.popleft()

            if name not in network:
                continue

            device = devices[name]

            if signal == HIGH and isinstance(device, Flipflop):
                continue

            new_signal = device.send_signal(signal, from_name)

            if name == final_module:
                for reg, val in device.register.items():
                    if val and not cycles[reg]:
                        cycles[reg] = i + 1

                        if all(cycles.values()):
                            return cycles

            for next_name in network[name]:
                q.append((new_signal, next_name, name))

    raise Exception("cycle not found")


def calc1(network: Dict[str, List[str]], devices: Dict[str, Device]) -> int:
    result = 0
    all_pulses = {
        HIGH: 0,
        LOW: 0,
    }
    for _ in range(1000):
        pulses = click(network, devices)

        all_pulses[HIGH] += pulses[HIGH]
        all_pulses[LOW] += pulses[LOW]
    result = all_pulses[HIGH] * all_pulses[LOW]
    return result


def calc2(network: Dict[str, List[str]], devices: Dict[str, Device]) -> int:
    result = 0
    cycles = find_cycle(network, devices)
    result = math.lcm(*list(cycles.values()))
    return result


if __name__ == "__main__":
    raw_data = read_data()
    network, devices = parse(raw_data)
    print(calc1(network, devices))
    network, devices = parse(raw_data)
    print(calc2(network, devices))
