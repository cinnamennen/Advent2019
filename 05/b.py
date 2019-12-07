from __future__ import annotations
import pprint
import re
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Dict, Union, Callable
from tqdm import trange

pp = pprint.PrettyPrinter(indent=4)


@dataclass
class Computer:
    memory: List[int] = field(default_factory=list)
    _position: int = 0
    broken: bool = field(default=False, init=False)
    mode: List[int] = field(default_factory=list)
    args: List[int] = field(default_factory=list)
    hard_input: int = None
    accumulated_output = ""

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

    def get_mode(self) -> int:
        return self.mode.pop(0)

    def get_args(self):
        while self.mode:
            mode = self.mode.pop(0)
            if mode == 0:
                read = self.read()
                read_ = self.memory[read]
                self.args.append(read_)
            elif mode == 1:
                self.args.append(self.read())
            else:
                raise RuntimeError(f"{mode} is not a valid mode")

    def add(self):
        if not self.args:
            raise RuntimeError("Need arguments to add")
        position = self.read()
        self.memory[position] = reduce(lambda x, y: x + y, self.args)
        # print(f'writing to {position}, {self.memory[position]}')
        self.args = []

    def multiply(self):
        if not self.args:
            raise RuntimeError("Need arguments to multiply")
        position = self.read()
        self.memory[position] = reduce(lambda x, y: x * y, self.args)
        # print(f'writing to {position}, {self.memory[position]}')
        self.args = []

    def halt(self):
        self.broken = True

    def _input(self):
        position = self.read()

        if self.hard_input is None:
            self.memory[position] = int(input(">"))
        else:
            self.memory[position] = self.hard_input

        # print(f'writing {self.memory[position]} to {position}')
        self.args = []

    def output(self):
        position = self.args[0]
        self.accumulated_output += str(position)
        # print(f'reading {self.memory[position]} from {position}')
        self.args = []

    def iterate(self):
        op = self.get_operation()
        # print(f'doing {op} with modes {self.mode}', end=' ')
        self.get_args()
        # print(f'args {self.args}')
        command = self.mapping[op]
        return command(self)

    def jit(self):
        if len(self.args) != 2:
            raise RuntimeError("Need arguments to jit")
        if self.args[0] != 0:
            # print(f'jumping to {self.args[1]} because {self.args[0]} != {0}')
            self.position = self.args[1]
        self.args = []

    def jif(self):
        if len(self.args) != 2:
            raise RuntimeError("Need arguments to jif")
        if self.args[0] == 0:
            # print(f'jumping to {self.args[1]} because {self.args[0]} == {0}')
            self.position = self.args[1]
        self.args = []

    def lt(self):
        if len(self.args) != 2:
            raise RuntimeError("Need arguments to lt")
        position = self.read()
        self.memory[position] = 1 if self.args[0] < self.args[1] else 0
        self.args = []

    def eq(self):
        if len(self.args) != 2:
            raise RuntimeError("Need arguments to lt")
        position = self.read()
        self.memory[position] = 1 if self.args[0] == self.args[1] else 0
        self.args = []

    def get_operation(self) -> int:
        op_code = self.read()
        if op_code in self.mapping.keys():
            # print(f'found {op_code} in {self.mapping.keys()}')
            op = op_code
        else:
            sop_code = str(op_code)
            args = list(sop_code[:-2])
            op = int(sop_code[-2:])
            while args:
                self.mode.append(int(args.pop()))

        while len(self.mode) < self.num_args[op]:
            self.mode.append(0)

        return op

    def run(self):
        while not self.broken:
            self.iterate()
            # print(self.memory, self.position)
        return self.accumulated_output

    mapping = {
        1: add,
        2: multiply,
        3: _input,
        4: output,
        5: jit,
        6: jif,
        7: lt,
        8: eq,
        99: halt,
    }

    num_args = {1: 2, 2: 2, 3: 0, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 99: 0}


def process_input():
    file = "a.txt"
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input(data: str = None):
    if not data:
        data = process_input()[0]
    data = list(map(int, data.split(",")))
    return data


def solve(data, i):
    return soft_solve(data, i)


def soft_solve(data, i):
    c = Computer(memory=get_input(data), hard_input=i)
    output = c.run()
    return output


def main():
    print(solve(None, 5))


if __name__ == "__main__":
    main()
