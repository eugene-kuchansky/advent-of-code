import sys
from typing import Tuple, NamedTuple, List, Dict
from collections import defaultdict


class Point(NamedTuple):
    x: int
    y: int


def read_data() -> List[Point]:
    raw_data = sys.stdin.read()
    points = []
    for coors in raw_data.split("\n"):
        x, y = coors.split(", ")
        p = Point(int(x), int(y))
        points.append(p)
    return points


def calc_all_distances_in_point(points: List[Point]) -> Dict[Point, List[Tuple[int, Point]]]:
    left = min(p.x for p in points) - 1
    right = max(p.x for p in points) + 1
    top = min(p.y for p in points) - 1
    bottom = max(p.y for p in points) + 1
    distances = defaultdict(list)
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            coord = Point(x, y)
            point_distances = sorted([(abs(coord.x - p.x) + abs(coord.y - p.y), p) for p in points])
            distances[coord] = point_distances

    return distances


def calc1(points: List[Point]) -> int:
    distances = calc_all_distances_in_point(points)
    closest = defaultdict(list)

    for coord, point_distances in distances.items():
        if point_distances[0][0] < point_distances[1][0]:
            n += point_distances[0][0] // 2
            closest[point_distances[0][1]].append(coord)

    max_area = 0
    left = min(p.x for p in points) - 1
    right = max(p.x for p in points) + 1
    top = min(p.y for p in points) - 1
    bottom = max(p.y for p in points) + 1

    for closest_points in closest.values():
        is_finite = True
        for point in closest_points:
            if point.x == left or point.x == right or point.y == top or point.y == bottom:
                is_finite = False
                break
        if is_finite:
            area = len(closest_points)
            if area > max_area:
                max_area = area

    return max_area


def calc2(points: List[Point], max_distance=10000) -> int:
    all_distances = calc_all_distances_in_point(points)
    closest_regions = 0
    for points_distances in all_distances.values():
        distances = sum(_[0] for _ in points_distances)
        if distances < max_distance:
            closest_regions += 1

    return closest_regions


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
