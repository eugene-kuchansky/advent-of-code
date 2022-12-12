from typing import Tuple, Dict
from collections import Counter, defaultdict


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


RAW = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def parse(raw: str) -> Tuple[str, Dict[str, str]]:
    lines = raw.splitlines()
    template = lines[0].strip()
    pair_insertion: Dict[str, str] = {item[0]: item[1] for item in [line.split(" -> ") for line in lines[2:]]}

    return template, pair_insertion


def process_template(template_pairs: Dict[str, int], pair_insertion: Dict[str, str]) -> Dict[str, int]:
    new_pairs: Dict[str, int] = defaultdict(int)

    for pair, pair_count in template_pairs.items():
        if pair not in pair_insertion:
            raise RuntimeError(f"pair {pair} not in pairs")
        # if pair AB produces element X it means that pair AB produces two new pairs AX and XB
        # n pairs AB produces n AX and n XB pairs
        new_element = pair_insertion[pair]
        new_pair1 = f"{pair[0]}{new_element}"
        new_pair2 = f"{new_element}{pair[1]}"
        new_pairs[new_pair1] += pair_count
        new_pairs[new_pair2] += pair_count

    return new_pairs


def calc(template: str, pair_insertion: Dict[str, str], steps: int) -> int:
    # split initial string of chars into pairs of chars
    template_pairs: Dict[str, int] = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        template_pairs[pair] += 1

    for _ in range(steps):
        template_pairs = process_template(template_pairs, pair_insertion)

    # count how many times an element is the first item in pairs
    # ACBC -> AC CB BC -> A=1, C=2, B=1
    # except C, the last element in template, its value has to be incremented by 1

    all_elements: Dict[str, int] = defaultdict(int)
    for pair, value in template_pairs.items():
        all_elements[pair[0]] += value
    all_elements[template[-1]] += 1

    elements = Counter(all_elements).most_common()
    most_common = elements[0][1]
    least_common = elements[-1][1]

    return most_common - least_common


template, pair_insertion = parse(RAW)
assert calc(template, pair_insertion, 10) == 1588
assert calc(template, pair_insertion, 40) == 2188189693529


if __name__ == "__main__":
    template, pair_insertion = parse(read_data())
    print(calc(template, pair_insertion, 10))
    print(calc(template, pair_insertion, 40))
