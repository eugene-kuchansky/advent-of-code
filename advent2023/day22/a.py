from collections import defaultdict, deque

FILENAME = "input.txt"


def parse_input(filename):
    with open(filename, "r") as input_file:
        return [
            [[int(num) for num in pos.split(",")] for pos in brick.split("~")]
            for brick in input_file.read().split("\n") if brick
        ]


def create_bricks(data):
    return [
        {
            (x, y, z)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            for z in range(z1, z2 + 1)
        }
        for (x1, y1, z1), (x2, y2, z2) in data
    ]


def hit_bottom(brick):
    return any(pos[-1] == 0 for pos in brick)


def simulate_fall(bricks):
    occupied = {}
    supports = {i: set() for i in range(len(bricks))}
    for i, brick in enumerate(bricks):
        next_pos = {(x, y, z - 1) for x, y, z in brick}
        intersected = {occupied[pos] for pos in next_pos if pos in occupied}
        while not intersected and not hit_bottom(next_pos):
            brick = next_pos
            next_pos = {(x, y, z - 1) for x, y, z in brick}
            intersected = {occupied[pos] for pos in next_pos if pos in occupied}
        occupied |= {pos: i for pos in brick}
        for parent in intersected:
            supports[parent].add(i)
    return supports


def supported_bricks(supports):
    supported = defaultdict(set)
    for parent, children in supports.items():
        for child in children:
            supported[child].add(parent)
    return supported


def part_one(supports, supported):
    return {
        parent
        for parent, children in supports.items()
        if not children or all(len(supported[child]) > 1 for child in children)
    }


def bfs(graph, supported, root):
    count = 0
    removed = set()
    queue = deque([root])
    while queue:
        current = queue.popleft()
        removed.add(current)
        for child in graph[current]:
            if not supported[child] - removed:
                count += 1
                queue.append(child)
    return count


def part_two(graph, supported, unsafe):
    return sum(bfs(graph, supported, brick) for brick in unsafe)


def main():
    data = parse_input(FILENAME)
    data.sort(key=lambda brick: brick[0][2])
    bricks = create_bricks(data)
    supports = simulate_fall(bricks)
    supported = supported_bricks(supports)
    safe = part_one(supports, supported)
    print(len(safe))
    unsafe = set(range(len(bricks))) - safe
    print(part_two(supports, supported, unsafe))


if __name__ == "__main__":
    main()
