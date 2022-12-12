from typing import List, Tuple, Dict
from dataclasses import dataclass, field

Point = Tuple[int, int, int]
Distance = Tuple[int, int, int]
RelativeDir = Tuple[int, int, int]
RelativeUp = Tuple[int, int, int]

PointDiff = Dict[Distance, int]
DiffPoint = Dict[int, Distance]

ROTATION_NUM = 4

ORIENT_NUM = 6

INITIAL_R_O = (0, 0)


def rotate(p, r):
    x, y, z = p
    return {
        0: (x, y, z),
        1: (z, y, -x),
        2: (-x, y, -z),
        3: (-z, y, x),
    }[r]


def orient(p, o):
    x, y, z = p
    return {
        0: (x, y, z),
        1: (x, -y, -z),
        2: (y, x, -z),
        3: (y, -x, z),
        4: (y, z, x),
        5: (y, -z, -x),
    }[o]


def transform_dir_up(r: int, o: int, point: Point) -> Point:
    new_point = orient(point, o)
    return rotate(new_point, r)


@dataclass
class Scanner:
    points: List[Point]
    distances: List[Dict[Tuple[int, int], DiffPoint]] = field(default_factory=list)
    rotate = 0
    orient = 0
    zero = (0, 0, 0)
    processed = False

    def __post_init__(self):
        self._init()

    def _init(self):
        orig_distances: List[PointDiff] = []
        for i, point in enumerate(self.points):
            orig_distance = {}
            for j, other_point in enumerate(self.points):
                orig_distance[j] = (point[0] - other_point[0], point[1] - other_point[1], point[2] - other_point[2])
            orig_distances.append(orig_distance)

        for i, point in enumerate(self.points):
            distance = {}
            for r in range(ROTATION_NUM):
                for o in range(ORIENT_NUM):
                    distance[(r, o)] = {}
                    for j, other_point in enumerate(self.points):
                        orig_diff = orig_distances[i][j]
                        diff = transform_dir_up(r, o, orig_diff)
                        distance[(r, o)][diff] = j
            self.distances.append(distance)

    def re_init(self, points: List[Point]):
        self.points = points
        self.distances = []
        self._init()


def get_diff(r: int, o: int, from_p: Point, to_p: Point) -> Point:
    new_p = transform_dir_up(r, o, to_p)
    dx, dy, dz = from_p[0] - new_p[0], from_p[1] - new_p[1], from_p[2] - new_p[2]
    return (dx, dy, dz)


def transform_coord(r, o, coord_diff: Point, orig_p: Point) -> Point:
    new_p = transform_dir_up(r, o, orig_p)
    dx, dy, dz = coord_diff
    return (dx + new_p[0], dy + new_p[1], dz + new_p[2])


def abs_dist_from_to(p1: Point, p2: Point) -> Point:
    return (abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]))


def match(point1_diff, point2_diff, r, o, i, j, scanner1, scanner2):
    common_points = point1_diff.intersection(point2_diff)

    if len(common_points) < 11:
        return False

    coord_diff = get_diff(r, o, scanner1.points[i], scanner2.points[j])

    zero2 = transform_coord(r, o, coord_diff, (0, 0, 0))

    only2_points_diff_coords = point2_diff - common_points

    only2_points = set()
    for only2_point_diff in only2_points_diff_coords:
        only2_point_ind = scanner2.distances[j][(r, o)][only2_point_diff]
        only2_point_orig = scanner2.points[only2_point_ind]
        only2_point = transform_coord(r, o, coord_diff, only2_point_orig)
        only2_points.add(only2_point)

    scanner2.rotate = r
    scanner2.orient = o
    scanner2.zero = zero2

    points = scanner1.points + list(only2_points)
    scanner1.re_init(points)

    scanner2.points = []

    return True


def find_common_points(scanner1: Scanner, scanner2: Scanner):
    for i, p1 in enumerate(scanner1.points):
        point1_diff = set(scanner1.distances[i][INITIAL_R_O].keys())

        for j, r_o in enumerate(scanner2.distances):
            for r, o in r_o:
                point2_diff = r_o[(r, o)].keys()
                if match(point1_diff, point2_diff, r, o, i, j, scanner1, scanner2):
                    return True

    return False


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


def parse_scanner(lines) -> Scanner:
    points = []
    for point in lines.splitlines()[1:]:
        x, y, z = tuple([int(coord) for coord in point.split(",")])
        points.append((x, y, z))

    return Scanner(points)


def parse(raw: str) -> List[Scanner]:
    return [parse_scanner(scanner) for scanner in raw.split("\n\n")]


def calc(scanners: List[Scanner]) -> int:
    unprocessed = {i for i in range(1, len(scanners))}

    while unprocessed:
        for i in range(len(scanners) - 1):
            for j in range(i + 1, len(scanners)):
                if i in unprocessed and j in unprocessed:
                    continue
                if i not in unprocessed and j not in unprocessed:
                    continue
                scanner = scanners[i]
                other_scanner = scanners[j]
                new_scanner = j
                if i in unprocessed:
                    scanner, other_scanner = other_scanner, scanner
                    new_scanner = i

                if not scanner.points:
                    continue

                if find_common_points(scanner, other_scanner):
                    unprocessed.remove(new_scanner)
                    break
    return len(scanners[0].points)


def calc2(scanners: List[Scanner]) -> int:
    max_distance = 0
    for i in range(len(scanners) - 1):
        scanner = scanners[i]
        for j in range(i + 1, len(scanners)):
            other_scanner = scanners[j]
            dist = manhattan_distance(scanner.zero, other_scanner.zero)
            if dist > max_distance:
                max_distance = dist

    return max_distance


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


RAW = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

SCANNERS = parse(RAW)
assert calc(SCANNERS) == 79
assert calc2(SCANNERS) == 3621

if __name__ == "__main__":
    raw = read_data()
    scanners = parse(raw)
    print(calc(scanners))
    print(calc2(scanners))
