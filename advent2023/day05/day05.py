import sys
from typing import List, Tuple, NamedTuple
from operator import attrgetter
import bisect


class RangeMap(NamedTuple):
    start: int
    end: int
    shift: int


class Range(NamedTuple):
    start: int
    end: int


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> Tuple[List[int], List[List[RangeMap]]]:
    maps = []
    seeds = [int(num) for num in lines[0].split(": ")[1].split(" ") if num]

    range_maps = []
    for line in lines[2:]:
        if ":" in line:
            maps.append(sorted_ranges(range_maps))
            range_maps = []
            continue

        dest_start, source_start, range_len = [int(num) for num in line.split(" ")]
        range_maps.append(
            RangeMap(
                start=source_start,
                end=source_start + range_len - 1,
                shift=dest_start - source_start,
            )
        )

    maps.append(sorted_ranges(range_maps))

    return seeds, maps


def sorted_ranges(range_maps: List[RangeMap]) -> List[RangeMap]:
    return sorted(range_maps, key=attrgetter("start"))


def find_next_location(location: int, range_maps: List[RangeMap]) -> int:
    range_ind = bisect.bisect(range_maps, location, key=attrgetter("start"))

    if range_ind == 0:
        return location

    dest_range: RangeMap = range_maps[range_ind - 1]
    if dest_range.end < location:
        return location

    return location + dest_range.shift


def calc1(seeds: List[int], maps: List[List[RangeMap]]) -> int:
    locations = []
    for seed in seeds:
        location = seed
        for range_maps in maps:
            location = find_next_location(location, range_maps)

        locations.append(location)

    return min(locations)


def find_next_ranges(ranges: List[Range], range_maps: List[RangeMap]) -> List[Range]:
    processed_ranges = []
    unprocessed_ranges = ranges

    for range_map in range_maps:
        new_unprocessed_ranges = []
        for range in unprocessed_ranges:
            processed_part, unprocessed_part = intersect_ranges(range, range_map)
            new_unprocessed_ranges.extend(unprocessed_part)
            processed_ranges.extend(processed_part)

        unprocessed_ranges = new_unprocessed_ranges

    processed_ranges.extend(unprocessed_ranges)
    return processed_ranges


def intersect_ranges(current_range: Range, dest_range: RangeMap) -> Tuple[List[Range], List[Range]]:
    processed_part = []
    unprocessed_part = []

    # not in range, current is on the left
    #   source
    #   ------   dest
    #            ----
    if current_range.end < dest_range.start:
        unprocessed_part.append(current_range)
        return processed_part, unprocessed_part

    # not in range, current is on the right
    #          source
    #   dest   ------
    #   ----
    if current_range.start > dest_range.end:
        unprocessed_part.append(current_range)
        return processed_part, unprocessed_part

    # current range completely inside dest range
    #       source
    #       ------
    #        dest
    #     -----------
    if current_range.start >= dest_range.start and current_range.end <= dest_range.end:
        processed_part.append(
            Range(
                start=current_range.start + dest_range.shift,
                end=current_range.end + dest_range.shift,
            )
        )
        return processed_part, unprocessed_part

    # left part of current range
    #    source
    #    |-----|-----
    #           dest
    #           -----
    inside_start = current_range.start
    if current_range.start < dest_range.start:
        unprocessed_part.append(
            Range(
                start=current_range.start,
                end=dest_range.start - 1,
            )
        )
        inside_start = dest_range.start

    # right part of current range
    #     source
    #    ---|-----|
    #  dest
    #  -----
    inside_end = current_range.end
    if current_range.end > dest_range.end:
        unprocessed_part.append(
            Range(
                start=dest_range.end + 1,
                end=current_range.end,
            )
        )
        inside_end = dest_range.end

    # inside part of current range
    #     source
    #  ---|-----|---
    #      dest
    #     -------
    processed_part.append(
        Range(
            start=inside_start + dest_range.shift,
            end=inside_end + dest_range.shift,
        )
    )
    return processed_part, unprocessed_part


def calc2(seeds: List[int], maps: List[List[RangeMap]]) -> int:
    seeds_iter = iter(seeds)
    seed_ranges = []

    for source_start, range_len in zip(seeds_iter, seeds_iter):
        seed_ranges.append(Range(start=source_start, end=source_start + range_len - 1))

    final_ranges = []

    for seed_range in seed_ranges:
        ranges = [seed_range]
        for range_maps in maps:
            ranges = find_next_ranges(ranges, range_maps)
        final_ranges.extend(ranges)

    return min(final_ranges, key=attrgetter("start")).start


if __name__ == "__main__":
    raw_data = read_data()
    seeds, maps = parse(raw_data)
    print(calc1(seeds, maps))
    print(calc2(seeds, maps))
