from __future__ import annotations

import pprint
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from multiprocessing import Process
from typing import Dict, List
import networkx

from cinnamon_tools.point import Point, zero_point, Direction

from common.computer import Computer, computer_from_string

pp = pprint.PrettyPrinter(indent=4)
debug = False


def read_input():
    file = "input.txt"
    with open(file) as f:
        return f.readlines()


def parse_input(data: str = None):
    if not data:
        data = read_input()
    else:
        data = data.splitlines()
    data = [_.strip() for _ in data]
    data = data[0]
    return data


class Status(Enum):
    WALL = 0
    MOVED = 1
    OXYGEN = 2
    UNEXPLORED = -1


class Movement(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Conversion(Enum):
    NORTH = Direction.UP
    SOUTH = Direction.DOWN
    WEST = Direction.LEFT
    EAST = Direction.RIGHT


@dataclass
class Robot:
    program: str
    position: Point = field(default=zero_point(2), init=False)
    facing: Direction = field(default=Direction.UP, init=False)
    computer: Computer = field(init=False)
    world: Dict[Point, Status] = field(default_factory=lambda: defaultdict(lambda: Status.UNEXPLORED), init=False)
    oxygen: Point = field(default=None, init=False)

    def __post_init__(self):
        self.computer = computer_from_string(self.program)
        self.p = Process(target=self.computer.run)
        self.p.start()

    def move(self):
        result = self.execute()
        probing = self.position + self.facing.value
        self.world[probing] = result
        if result == Status.WALL:
            self.facing = self.facing.prev()
        else:
            self.position = probing
            if result == Status.OXYGEN:
                self.oxygen = self.position

    def execute(self) -> Status:
        signal = Movement[Conversion(self.facing).name].value
        self.computer.data_in.put(signal)
        return Status(self.computer.data_out.get())

    def iterate(self):
        self.explore()
        if self.world[self.position + self.facing.next().value] == Status.WALL:
            # There is a wall to our right, move forward
            self.move()
        else:
            self.facing = self.facing.next()
            self.move()

    def print_hull(self):
        min_x = min(map(lambda p: p.x, self.world.keys()))
        min_y = min(map(lambda p: p.y, self.world.keys()))
        max_x = max(map(lambda p: p.x, self.world.keys()))
        max_y = max(map(lambda p: p.y, self.world.keys()))
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                status = self.world[Point(x, y)]
                if status == Status.WALL:
                    print("██", end='')
                elif status == Status.MOVED:
                    print("░░", end='')
                elif status == Status.OXYGEN:
                    print("()", end='')
                else:
                    print("  ", end='')

            print()

    def run(self):
        while not (self.computer.broken or self.oxygen):
            self.iterate()
        self.p.terminate()
        self.print_hull()

    def explore(self):
        # Pick an unexplored direction and move there
        explorable: List[Point] = [d for d in Direction if self.world[self.position + d.value] == Status.UNEXPLORED]
        for d in explorable:
            self.check_out(d)

    def check_out(self, d: Direction):
        old_direction = self.facing
        old_position = self.position
        self.facing = d
        self.move()
        self.facing = d.next().next()
        if old_position != self.position:
            self.move()
        self.facing = old_direction


def solve(data=None):
    data = parse_input(data)
    r = Robot(data)
    r.run()
    g = networkx.Graph()
    paths = []
    for k, v in r.world.items():
        if v == Status.MOVED or v == Status.OXYGEN:
            paths.append(k)
    for n in paths:
        g.add_node(n)
        for d in Direction:
            p = d.value + n
            if r.world[p] == Status.MOVED or r.world[p] == Status.OXYGEN:
                g.add_edge(n, p)

    return networkx.shortest_path_length(g, zero_point(2), r.oxygen)


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
