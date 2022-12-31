import sys
from typing import List, NamedTuple, Dict, Tuple
from collections import defaultdict


class Interval(NamedTuple):
    from_time: int
    to_time: int


class Guard(NamedTuple):
    id: int
    sleeps: Dict[str, Interval]


def read_data() -> List[Guard]:
    raw_data = sys.stdin.read().split("\n")
    raw_data = sorted(raw_data)
    guards: Dict[str, Interval] = defaultdict(lambda: defaultdict(list))
    guard_id = 0
    from_time = 0
    # sleeps = defaultdict(list)
    for row in raw_data:
        items = row.split(" ")
        date = items[0][1:]
        time = int(items[1][:-1].split(":")[1])
        if items[2] == "Guard":
            #     if guard_id:
            #         guard = Guard(id=guard_id, sleeps=sleeps)
            #         guards.append(guard)
            guard_id = int(items[3][1:])
        #     sleeps = defaultdict(list)
        if items[2] == "falls":
            from_time = time
        elif items[2] == "wakes":
            guards[guard_id][date].append(Interval(from_time, time))
    return [Guard(guard_id, sleeps) for guard_id, sleeps in guards.items()]
    # guard = Guard(id=guard_id, sleeps=sleeps)
    # guards.append(guard)
    # for guard in sorted(guards, key=lambda x: x.id):
    #     print(guard)
    # exit()
    # for item in raw_data.split("\n"):
    #     id_data, _, pos_data, size_data = item.split(" ")
    #     _, id_ = id_data.split("#")
    #     col, row = pos_data[:-1].split(",")
    #     w, h = size_data.split("x")
    #     rectangles.append(Rect(int(id_), int(col), int(row), int(w), int(h)))

    return guards


def get_most_sleep_minute(sleeps: Dict[str, Interval]) -> Tuple[int, int]:
    minutes = {i: 0 for i in range(60)}

    for day_sleeps in sleeps.values():
        for sleep in day_sleeps:
            for i in range(sleep.from_time, sleep.to_time):
                minutes[i] += 1
    return sorted([(sleep, minute) for minute, sleep in minutes.items()], reverse=True)[0]


def calc1(guards: List[Guard]) -> int:
    max_sleep_total = 0
    guard_id = 0

    for guard in guards:
        total_sleep = sum(sleep.to_time - sleep.from_time for sleeps in guard.sleeps.values() for sleep in sleeps)
        if total_sleep > max_sleep_total:
            max_sleep_total = total_sleep
            guard_id = guard.id
    for guard in guards:
        if guard.id == guard_id:
            _, minute = get_most_sleep_minute(guard.sleeps)
            return minute * guard.id
    return 0


def calc2(guards: List[Guard]) -> int:
    minute_of_max_asleep = 0
    max_sleep_times = 0
    guard_id = 0

    for guard in guards:
        sleep_times, minute = get_most_sleep_minute(guard.sleeps)
        if sleep_times > max_sleep_times:
            max_sleep_times = sleep_times
            minute_of_max_asleep = minute
            guard_id = guard.id

    return minute_of_max_asleep * guard_id


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
