import sys
from typing import Set, List, Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class Sensor:
    x: int
    y: int

    beacon_x: int
    beacon_y: int

    dist: int

    @staticmethod
    def get_coord(s: str) -> Tuple[int, int]:
        _, data = s.split("at ")
        x_data, y_data = data.split(", ")
        _, x = x_data.split("=")
        _, y = y_data.split("=")
        return int(x), int(y)

    @staticmethod
    def get_distance_to(x, y, beacon_x, beacon_y) -> int:
        return abs(x - beacon_x) + abs(y - beacon_y)

    @classmethod
    def from_str(cls, sensor_coord: str, beacon_coord) -> "Sensor":
        x, y = cls.get_coord(sensor_coord)
        beacon_x, beacon_y = cls.get_coord(beacon_coord)
        return cls(x, y, beacon_x, beacon_y, cls.get_distance_to(x, y, beacon_x, beacon_y))


def read_data() -> List[Sensor]:
    raw_data = sys.stdin.read()
    sensors: List[Sensor] = []
    for line in raw_data.split("\n"):
        sensor_data, beacon_data = line.split(": ")
        sensor = Sensor.from_str(sensor_data, beacon_data)
        sensors.append(sensor)
    return sensors


def get_line_coverage(sensors: List[Sensor], line_y: int) -> List[Tuple[int, int]]:
    coverage: List[Tuple[int, int]] = []
    for sensor in sensors:
        dist_to_line = abs(sensor.y - line_y)
        rest_dist = sensor.dist - dist_to_line
        if rest_dist < 0:
            continue

        start_x = sensor.x - rest_dist
        finish_x = sensor.x + rest_dist

        coverage.append((start_x, finish_x))

    coverage = sorted(coverage)
    start = 0
    end = 1
    merged_coverage = [coverage[0]]
    for line in coverage[1:]:
        last_line = merged_coverage[-1]

        if (last_line[end] + 1) < line[start]:
            merged_coverage.append(line)
            continue
        new_line_end = max(last_line[end], line[end])
        merged_coverage[-1] = (last_line[start], new_line_end)

    return merged_coverage


def calc1(sensors: List[Sensor]) -> int:
    if len(sensors) == 14:
        line_y = 10
    else:
        line_y = 2000000

    coverage = get_line_coverage(sensors, line_y)

    beacons_on_line: Set[int] = set()
    for sensor in sensors:
        if sensor.beacon_y == line_y:
            beacons_on_line.add(sensor.beacon_x)

    not_possible_places = 0

    for start_x, finish_x in coverage:
        not_possible_places += finish_x - start_x + 1
        for beacon_x in beacons_on_line:
            if finish_x >= beacon_x >= start_x:
                not_possible_places -= 1
    return not_possible_places


def calc2(sensors: List[Sensor]) -> int:
    if len(sensors) == 14:
        max_line_y = 20
    else:
        max_line_y = 4000000

    for line_y in range(max_line_y):
        if line_y % 100000 == 0:
            print(f"{line_y} of {max_line_y}")
        coverage = get_line_coverage(sensors, line_y)

        if len(coverage) == 2:
            x = coverage[0][1] + 1
            return x * 4000000 + line_y
    return 0


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
