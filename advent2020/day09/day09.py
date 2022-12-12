import sys
from typing import List, Iterable, Dict, NamedTuple, Optional
from collections import defaultdict


PREAMBLE_LEN = 25

IndexType = int
SumType = int
ValueType = int


class Pair(NamedTuple):
    index1: IndexType
    index2: IndexType


def read_data(stream: Iterable[str]) -> List[ValueType]:
    return [ValueType(line) for line in stream if line.strip()]


# way too complex. in the context of size of data this solution should be brutforce-ish
# the idea behind this solution:
# - keep all sums of combination of preamble elements
#   this allows to avoid recalculation of pairs which are not changed
# - keep links sum->pairs
#   when first element is removed then it's sums with other elements are removed without recalculation
class Preamble:
    def __init__(self):
        self.index_sums: Dict[IndexType, Dict[SumType, List[IndexType]]] = {}
        self.index_values: Dict[IndexType, ValueType] = {}
        self.sum_pairs: Dict[SumType, List[Pair]] = defaultdict(list)

    def _update_links(self, ind: IndexType, other_ind: IndexType, new_sum: SumType):
        sum_items = self.index_sums[ind].get(new_sum, [])
        sum_items.append(other_ind)
        self.index_sums[ind][new_sum] = sum_items

    def add(self, new_ind: IndexType, new_value: ValueType):
        self.index_sums[new_ind] = {}
        for ind, value in self.index_values.items():
            new_sum = value + new_value
            self.sum_pairs[new_sum].append(Pair(new_ind, ind))

            self._update_links(new_ind, ind, new_sum)
            self._update_links(ind, new_ind, new_sum)
        self.index_values[new_ind] = new_value

    def _remove_sum_pairs(self, old_ind: IndexType, old_sum: SumType):
        old_pairs = self.sum_pairs[old_sum]
        pairs = [pair for pair in old_pairs if (pair.index1 != old_ind and pair.index2 != old_ind)]
        if not pairs:
            del self.sum_pairs[old_sum]
        else:
            self.sum_pairs[old_sum] = pairs

    def _remove_links(self, ind: IndexType,  old_ind: IndexType, old_sum: SumType):
        old_sum_items = self.index_sums[ind][old_sum]
        sum_items = [item for item in old_sum_items if item != old_ind]
        if not sum_items:
            del self.index_sums[ind][old_sum]
        else:
            self.index_sums[ind][old_sum] = sum_items

    def remove(self, old_ind: IndexType):
        for old_sum, sum_items in self.index_sums[old_ind].items():
            self._remove_sum_pairs(old_ind, old_sum)
            for ind in sum_items:
                self._remove_links(ind, old_ind, old_sum)

        del self.index_sums[old_ind]
        del self.index_values[old_ind]

    def is_in_sums(self, value: SumType) -> bool:
        return value in self.sum_pairs


def calc1(numbers: List[ValueType], preamble_len: int) -> int:
    preamble = Preamble()
    for i in range(preamble_len):
        preamble.add(i, numbers[i])

    for i in range(preamble_len, len(numbers)):
        next_number = numbers[i]
        if not preamble.is_in_sums(next_number):
            return i
        preamble.remove(i - preamble_len)
        preamble.add(i, numbers[i])

    return -1


# one again this solution is pre-optimized
# premature optimization is the root of all evil (c) Donald Knuth
# it would be sufficient to check sequences which start at every number
# until sum ot elements if not more that target number
def calc2(target_value_ind: IndexType, numbers: List[ValueType]) -> List[ValueType]:
    target_value = numbers[target_value_ind]

    available_sets: List[List[ValueType]] = []
    start_ind: Optional[int] = None

    # search for all contiguous sets with length more than 2 containing lesser than target value numbers
    for i, value in enumerate(numbers):
        if value < target_value:
            if start_ind is None:
                start_ind = i
            continue
        if start_ind is not None and i - start_ind > 1:
            available_sets.append(numbers[start_ind: i - 1])
        start_ind = None

    if start_ind is not None and len(numbers) - start_ind > 1:
        available_sets.append(numbers[start_ind:])

    for available_set in available_sets:
        res = check_set(available_set, target_value)
        if res:
            return res
    return []


def check_set(available_set: List[ValueType], target_value: ValueType) -> List[ValueType]:
    for start_ind, value in enumerate(available_set[:-1]):
        current_sum = available_set[start_ind]
        for end_ind in range(start_ind + 1, len(available_set)):
            current_sum += available_set[end_ind]
            if current_sum == target_value:
                return available_set[start_ind: end_ind + 1]
            if current_sum > target_value:
                break
    return []


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data, PREAMBLE_LEN)
    print(f"result 1: {initial_data[res1]}, {res1}")

    res2 = calc2(res1, initial_data)
    print(f"result 2: {min(res2) + max(res2)}")
