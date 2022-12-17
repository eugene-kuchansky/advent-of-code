import sys
from typing import List, Tuple, Dict
from dataclasses import dataclass
import heapq


@dataclass
class Valve:
    name: str
    rate: int
    leads_to: List[str]


def read_data() -> Dict[str, Valve]:
    valves: Dict[str, Valve] = {}
    raw_data = sys.stdin.read()
    for line in raw_data.split("\n"):
        tunnel, leads_to = line.split("; ")
        _, tunnel_name, _, _, rate_data = tunnel.split(" ")
        rate = int(rate_data.split("=")[1])
        if "valves" in leads_to:
            split_by = "valves "
        else:
            split_by = "valve "
        tunnels = leads_to.split(split_by)[1].split(", ")
        valve = Valve(tunnel_name, rate, tunnels)
        valves[valve.name] = valve

    return valves


def get_all_paths(valves: Dict[str, Valve], max_minutes) -> Dict[Tuple, int]:
    start = "AA"
    valves_names = list(valves.keys())
    valve_to_ind = {valve: i for i, valve in enumerate(valves_names)}

    dist = [[float("inf") for _ in range(len(valves_names))] for _ in range(len(valves_names))]

    for i in range(len(valves_names)):
        dist[i][i] = 0

    for valve_name, valve in valves.items():
        from_ind = valve_to_ind[valve_name]
        for to_valve in valve.leads_to:
            to_ind = valve_to_ind[to_valve]
            dist[from_ind][to_ind] = 1
            dist[to_ind][from_ind] = 1

    for k in range(len(valves_names)):
        for i in range(len(valves_names)):
            for j in range(len(valves_names)):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    q: List[Tuple] = [(0, 0, start, [start])]

    paths: Dict[Tuple, int] = {
        (start,): 0,
    }
    while q:
        minutes, total_rate, from_valve, path = heapq.heappop(q)
        from_ind = valve_to_ind[from_valve]

        paths[tuple(path)] = -total_rate

        for to_valve in valves_names:
            if to_valve == from_valve:
                continue
            if to_valve in path:
                continue

            if valves[to_valve].rate == 0:
                continue

            distance_in_minutes = dist[valve_to_ind[from_valve]][valve_to_ind[to_valve]]
            new_minutes = minutes + distance_in_minutes + 1

            if new_minutes > max_minutes:
                continue

            new_total_rate = total_rate - valves[to_valve].rate * (max_minutes - new_minutes)
            new_path = list(path)
            new_path.append(to_valve)
            heapq.heappush(q, (new_minutes, new_total_rate, to_valve, new_path))
    return paths


def get_all_paths2(valves: Dict[str, Valve], max_minutes) -> Dict[Tuple, int]:
    start = "AA"
    valves_names = list(valves.keys())
    valve_to_ind = {valve: i for i, valve in enumerate(valves_names)}

    dist = [[float("inf") for _ in range(len(valves_names))] for _ in range(len(valves_names))]

    for i in range(len(valves_names)):
        dist[i][i] = 0

    for valve_name, valve in valves.items():
        from_ind = valve_to_ind[valve_name]
        for to_valve in valve.leads_to:
            to_ind = valve_to_ind[to_valve]
            dist[from_ind][to_ind] = 1
            dist[to_ind][from_ind] = 1

    for k in range(len(valves_names)):
        for i in range(len(valves_names)):
            for j in range(len(valves_names)):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    paths: Dict[Tuple, int] = {
        (start,): 0,
    }

    minutes = max_minutes
    pressure = 0
    from_valve = start
    path = [start]
    s = []
    s.append((minutes, pressure, from_valve, path))

    while s:
        minutes, pressure, from_valve, path = s.pop(0)
        from_ind = valve_to_ind[from_valve]

        paths[tuple(path)] = pressure

        for to_valve in valves_names:
            if to_valve in path or valves[to_valve].rate == 0:
                continue
            to_ind = valve_to_ind[to_valve]
            distance_in_minutes = dist[from_ind][to_ind] + 1

            if minutes <= distance_in_minutes:
                continue

            new_minutes = minutes - distance_in_minutes

            new_pressure = pressure + valves[to_valve].rate * new_minutes
            new_path = list(path)
            new_path.append(to_valve)
            paths[tuple(new_path)] = new_pressure

            s.append((new_minutes, new_pressure, to_valve, new_path))
    return paths


def calc1(valves: Dict[str, Valve]) -> int:
    paths = get_all_paths(valves, max_minutes=30)
    max_pressure = max(paths.values())

    # for path in paths:
    #     if paths[path] == max_pressure:
    #         print(path, max_pressure)
    return max_pressure


def calc2(valves: Dict[str, Valve]) -> int:
    paths = get_all_paths(valves, max_minutes=26)
    sorted_paths = sorted([(pressure, path) for path, pressure in paths.items()], reverse=True)

    max_pressure = 0
    for i, (pressure1, path1) in enumerate(sorted_paths):
        path1 = set(path1[1:])
        for pressure2, path2 in sorted_paths[i + 1 :]:
            if pressure1 + pressure2 <= max_pressure:
                break
            path2 = set(path2[1:])
            if len(set.intersection(path1, path2)) == 0:
                if pressure1 + pressure2 > max_pressure:
                    max_pressure = pressure1 + pressure2
    return max_pressure


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
