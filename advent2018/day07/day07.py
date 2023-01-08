import sys
from typing import Tuple, List, Dict, Set
from collections import defaultdict

import heapq


def read_data() -> Dict[str, Set[str]]:
    raw_data = sys.stdin.read()
    deps = defaultdict(set)
    for row in raw_data.split("\n"):
        dep_data = row.split(" ")
        step = dep_data[1]
        dependant_step = dep_data[7]
        deps[step].add(dependant_step)

    return deps


def get_depends_on(deps: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    depends_on: Dict[str, Set[str]] = defaultdict(set)
    for step, dependant_steps in deps.items():
        for dep_step in dependant_steps:
            depends_on[dep_step].add(step)
            if step not in depends_on:
                depends_on[step] = set()
    return depends_on


def calc1(dependance_for: Dict[str, Set[str]]) -> str:
    depends_on = get_depends_on(dependance_for)

    steps: List[str] = []
    for step, depends_on_steps in depends_on.items():
        if not depends_on_steps:
            steps.append(step)
    heapq.heapify(steps)

    completed_steps: Set[str] = set()
    steps_order: List[str] = []
    while steps:
        new_steps: List[str] = []
        while True:
            step = heapq.heappop(steps)
            depends_on[step] = depends_on[step] - completed_steps
            if not depends_on[step]:
                steps_order.append(step)
                completed_steps.add(step)
                for old_step in steps:
                    new_steps.append(old_step)

                for new_step in dependance_for[step]:
                    if new_step not in new_steps:
                        new_steps.append(new_step)
                break
            new_steps.append(step)

        heapq.heapify(new_steps)
        steps = new_steps

    return "".join(steps_order)


def step_to_time(step: str, base=60) -> int:
    return ord(step) - ord("A") + base


def calc2(dependance_for: Dict[str, Set[str]]) -> int:
    max_workers = 5
    base_sleep = 61
    depends_on = get_depends_on(dependance_for)

    steps: List[str] = []
    for step, depends_on_steps in depends_on.items():
        if not depends_on_steps:
            steps.append(step)
    heapq.heapify(steps)

    completed_steps: Set[str] = set()
    steps_order: List[str] = []
    current_time = 0
    workers: List[Tuple[int, str]] = []

    while steps and len(workers) < max_workers:

        new_steps: List[str] = []
        while steps and len(workers) < max_workers:
            step = heapq.heappop(steps)
            depends_on[step] = depends_on[step] - completed_steps
            if not depends_on[step]:
                heapq.heappush(workers, (step_to_time(step, base=base_sleep), step))
            else:
                new_steps.append(step)

        for old_step in steps:
            new_steps.append(old_step)

        time, step = heapq.heappop(workers)
        steps_order.append(step)
        completed_steps.add(step)

        for new_step in dependance_for[step]:
            if new_step not in new_steps:
                new_steps.append(new_step)
        current_time += time
        workers = [(w_time - time, w_step) for w_time, w_step in workers]

        heapq.heapify(new_steps)
        steps = new_steps

    return current_time


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
