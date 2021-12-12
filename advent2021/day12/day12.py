from typing import List, Dict, DefaultDict
from dataclasses import dataclass, field
from collections import defaultdict


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

RAW2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

RAW3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

START = "start"
END = "end"


@dataclass
class Caves:
    graph: DefaultDict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    paths: List[List[str]] = field(default_factory=list)

    def add_path(self, cave1: str, cave2: str):
        self.graph[cave1].append(cave2)
        self.graph[cave2].append(cave1)

    def find_all_paths(self, can_re_visit: bool):
        visited: Dict[str, int] = defaultdict(int)
        path: List[str] = []
        self.search(START, visited, path, can_re_visit)

    def search(self, cave: str, visited: Dict[str, int], path: List[str], can_re_visit: bool):
        path.append(cave)

        if cave == END:
            self.paths.append(path.copy())
            path.pop()
            return

        if cave.islower():
            visited[cave] += 1

        for neighbor in self.graph[cave]:
            if neighbor == START:
                continue
            if neighbor == path[-1]:
                continue
            if visited[neighbor]:
                if not (can_re_visit and 2 not in visited.values()):
                    continue
            self.search(neighbor, visited, path, can_re_visit)

        path.pop()
        if cave.islower():
            visited[cave] -= 1


def parse(raw: str) -> Caves:
    caves = Caves()
    for line in raw.splitlines():
        path = line.split("-")
        caves.add_path(path[0], path[1])

    return caves


def calc(caves: Caves) -> int:
    caves.find_all_paths(can_re_visit=False)
    return len(caves.paths)


def calc2(caves: Caves) -> int:
    caves.find_all_paths(can_re_visit=True)
    return len(caves.paths)


assert calc(parse(RAW)) == 10
assert calc(parse(RAW2)) == 19
assert calc(parse(RAW3)) == 226

assert calc2(parse(RAW)) == 36
assert calc2(parse(RAW2)) == 103
assert calc2(parse(RAW3)) == 3509


if __name__ == "__main__":
    raw_data = read_data()
    print(calc(parse(raw_data)))
    print(calc2(parse(raw_data)))
