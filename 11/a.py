from __future__ import annotations
import pprint
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from queue import Queue
from typing import List, Dict
from cinnamon_tools.point import Point, zero_point, Direction

from common.computer import Computer, Memory

pp = pprint.PrettyPrinter(indent=4)
debug = False


class Paint(Enum):
    BLACK = 0
    WHITE = 1


def default_field(obj):
    return field(default_factory=lambda: obj)


@dataclass
class Robot:
    program: str
    position: Point = field(default=zero_point(2), init=False)
    hull: Dict[Point, Paint] = field(
        default_factory=lambda: defaultdict(lambda: Paint.BLACK), init=False
    )
    facing: Direction = field(default=Direction.UP, init=False)
    computer: Computer = field(init=False)

    def __post_init__(self):
        self.computer = Computer(Memory(map(int, self.program.split(","))))

    def scan(self):
        self.computer.data_in.put(self.hull[self.position].value)

    def paint(self):
        self.hull[self.position] = Paint(self.computer.data_out.get())

    def move(self):
        self.position += self.facing.value

    def turn(self):
        get = self.computer.data_out.get()
        self.facing = self.facing.prev() if get == 0 else self.facing.next()

    def iterate(self):
        self.scan()
        self.paint()
        self.turn()
        self.move()

    def run(self):
        threading.Thread(target=self.computer.run).start()
        while not self.computer.broken:
            self.iterate()
        return self.hull


def process_input():
    file = "a.txt"
    with open(file) as f:
        data = f.readlines()
    data = [_.strip() for _ in data]
    return data


def get_input(data: str = None):
    if not data:
        data = process_input()[0]
    return data


def solve(data=None):
    s = get_input(data)
    robot = Robot(s)
    return robot.run()


def main():
    print(len(solve()))


if __name__ == "__main__":
    main()
