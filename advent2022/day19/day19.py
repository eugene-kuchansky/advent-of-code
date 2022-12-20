import sys
from typing import Dict, Set, List
from dataclasses import dataclass, astuple
import re
from functools import total_ordering


@total_ordering
@dataclass
class Resource:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other: "Resource") -> "Resource":
        return Resource(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def __sub__(self, other: "Resource") -> "Resource":
        return Resource(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode,
        )

    def __lt__(self, other: "Resource") -> bool:
        return (
            self.ore <= other.ore
            and self.clay <= other.clay
            and self.obsidian <= other.obsidian
            and self.geode <= other.geode
        )


@dataclass(frozen=True)
class Blueprint:
    id: int
    ore: Resource
    clay: Resource
    obsidian: Resource
    geode: Resource


def read_data() -> List[Blueprint]:
    raw_data = sys.stdin.read()
    blueprints: List[Blueprint] = []
    for line in raw_data.split("\n"):
        numbers = [int(_) for _ in re.findall(r"\d+", line)]

        bp = Blueprint(
            id=numbers[0],
            ore=Resource(ore=numbers[1]),
            clay=Resource(ore=numbers[2]),
            obsidian=Resource(ore=numbers[3], clay=numbers[4]),
            geode=Resource(ore=numbers[5], obsidian=numbers[6]),
        )
        blueprints.append(bp)

    return blueprints


@dataclass
class State:
    robots: Resource
    resources: Resource
    prev_can_ore: bool
    prev_can_clay: bool
    prev_can_obsidian: bool


@dataclass
class Factory:
    bp: Blueprint

    def process(self, max_minutes) -> int:

        states: List[List[State]] = [list() for _ in range(max_minutes + 1)]

        ore = Resource(ore=1)
        clay = Resource(clay=1)
        obsidian = Resource(obsidian=1)
        geode = Resource(geode=1)

        max_ore: int = max(self.bp.ore.ore, self.bp.clay.ore, self.bp.obsidian.ore, self.bp.geode.ore)
        max_clay = self.bp.obsidian.clay
        max_obsidian = self.bp.geode.obsidian

        s = State(
            robots=Resource(ore=1),
            resources=Resource(),
            prev_can_ore=False,
            prev_can_clay=False,
            prev_can_obsidian=False,
        )
        states[0].append(s)

        for minute in range(0, max_minutes):
            max_genodes = max(state.resources.geode for state in states[minute])
            for state in states[minute]:
                if max_genodes > state.resources.geode:
                    continue

                if self.bp.geode <= state.resources:
                    states[minute + 1].append(
                        State(
                            robots=state.robots + geode,
                            resources=state.resources + state.robots - self.bp.geode,
                            prev_can_ore=False,
                            prev_can_clay=False,
                            prev_can_obsidian=False,
                        )
                    )
                    continue
                can_ore = self.bp.ore <= state.resources and state.robots.ore <= max_ore
                can_clay = self.bp.clay <= state.resources and state.robots.clay <= max_clay
                can_obsidian = self.bp.obsidian <= state.resources and state.robots.obsidian <= max_obsidian

                states[minute + 1].append(
                    State(
                        robots=state.robots,
                        resources=state.resources + state.robots,
                        prev_can_ore=can_ore,
                        prev_can_clay=can_clay,
                        prev_can_obsidian=can_obsidian,
                    )
                )
                if can_ore and not state.prev_can_ore:
                    states[minute + 1].append(
                        State(
                            robots=state.robots + ore,
                            resources=state.resources + state.robots - self.bp.ore,
                            prev_can_ore=False,
                            prev_can_clay=False,
                            prev_can_obsidian=False,
                        )
                    )
                if can_clay and not state.prev_can_clay:
                    states[minute + 1].append(
                        State(
                            robots=state.robots + clay,
                            resources=state.resources + state.robots - self.bp.clay,
                            prev_can_ore=False,
                            prev_can_clay=False,
                            prev_can_obsidian=False,
                        )
                    )
                if can_obsidian and not state.prev_can_obsidian:
                    states[minute + 1].append(
                        State(
                            robots=state.robots + obsidian,
                            resources=state.resources + state.robots - self.bp.obsidian,
                            prev_can_ore=False,
                            prev_can_clay=False,
                            prev_can_obsidian=False,
                        )
                    )

        return max(state.resources.geode for state in states[max_minutes])


def calc1(blueprints: List[Blueprint]) -> int:
    result = 0
    for bp in blueprints:
        factory = Factory(bp)
        max_geodes = factory.process(max_minutes=24)
        result += max_geodes * bp.id
    return result


def calc2(blueprints: List[Blueprint]) -> int:
    result = 1
    for bp in blueprints[:3]:
        factory = Factory(bp)
        max_geodes = factory.process(max_minutes=32)
        result *= max_geodes
    return result


if __name__ == "__main__":
    data = read_data()
    print(calc1(data))
    print(calc2(data))
