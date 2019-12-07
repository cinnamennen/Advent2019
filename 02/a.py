from __future__ import annotations
import pprint
import re
from dataclasses import dataclass, field
from typing import List, Dict, Union, Callable

pp = pprint.PrettyPrinter(indent=4)


@dataclass
class Computer:
    memory: List[int] = field(default_factory=list)
    _position: int = 0
    broken: bool = field(default=False, init=False)

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, v: int) -> None:
        self._position = v

    def read(self) -> int:
        rv = self.memory[self.position]
        self.position += 1
        return rv

    def halt(self):
        self.broken = True

    def add(self):
        a = self.read()
        b = self.read()
        position = self.read()
        self.memory[position] = self.memory[a] + self.memory[b]

    def multiply(self):
        a = self.read()
        b = self.read()
        position = self.read()
        self.memory[position] = self.memory[a] * self.memory[b]

    def iterate(self):
        op = self.read()
        command = self.mapping[op]
        return command(self)

    def run(self):
        while not self.broken:
            self.iterate()

    mapping = {1: add, 2: multiply, 99: halt}


def process_input():
    file = "a.txt"
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input(data: str = None):
    if not data:
        data = process_input()[0]
    data = list(map(int, data.split(",")))
    return Computer(memory=data)


def soft_solve(data):
    c = get_input(data)
    c.run()
    return c.memory


def solve(data=None) -> int:
    c = get_input(data)
    c.memory[1] = 12
    c.memory[2] = 2
    c.run()
    return c.memory[0]


def main():
    print(solve())


if __name__ == "__main__":
    main()
