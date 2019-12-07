from __future__ import annotations
import pprint
import re
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Dict, Union, Callable, Tuple, Set

from cinnamon_tools.point import Point, zero_point, directions

pp = pprint.PrettyPrinter(indent=4)


def process_input() -> List[str]:
    file = "a.txt"
    data = [_.strip() for _ in open(file).readlines()]
    return data


Instruction = Tuple[str, int]

short_mapping = {"L": "left", "R": "right", "U": "up", "D": "down"}


def split_instruction(s: str) -> Instruction:
    return short_mapping[s[0]], int(s[1:])


def get_input(data: List[str] = None):
    if not data:
        data = process_input()
    data = [x.split(",") for x in data]
    data = [list(map(split_instruction, x)) for x in data]

    return data


def make_wire(instructions: List[Instruction]) -> set:
    current = zero_point(2)
    wire = {current}
    for direction, distance in instructions:
        for i in range(1, distance + 1):
            current += directions[direction]
            wire.add(current)
    return wire


def get_intersections(data: List[List[Tuple[str, int]]]) -> Set[Point]:
    wires = list(map(make_wire, data))
    r = reduce(set.intersection, wires)
    r.remove(zero_point(2))
    return r


def get_distances(data) -> List[int]:
    intersections = get_intersections(data)
    return list(map(Point.zero_distance, intersections))


def solve(data: List[str] = None) -> int:
    data = get_input(data)
    r = get_distances(data)
    return min(r)


def main():
    print(solve())


if __name__ == "__main__":
    main()
