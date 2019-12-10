from __future__ import annotations
import pprint
import threading
from dataclasses import dataclass, field
from functools import reduce
from queue import Queue
from typing import List
from itertools import permutations

from tqdm import tqdm

pp = pprint.PrettyPrinter(indent=4)


class Memory(list):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except IndexError:
            missing = key - (len(self) - 1)
            self += [0]*missing
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        try:
            return super().__setitem__(key, value)
        except IndexError:
            missing = key - (len(self) - 1)
            self += [0]*missing
            return super().__setitem__(key, value)


@dataclass
class Computer:
    memory: Memory[int]
    position: int = 0
    relative_base: int = 0
    broken: bool = field(default=False, init=False)
    mode: List[int] = field(default_factory=list, init=False)
    args: List[int] = field(default_factory=list, init=False)
    data_in: Queue = field(default_factory=Queue, init=False)
    data_out: Queue = field(default_factory=Queue, init=False)

    # @property
    # def position(self) -> int:
    #     return self._position
    #
    # @position.setter
    # def position(self, v: int) -> None:
    #     self._position = v

    def __copy__(self):
        return type(self)(self.memory)

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
                position = self.read()
                self.args.append(self.memory[position])
            elif mode == 1:
                self.args.append(self.read())
            elif mode == 2:
                position = self.read() + self.relative_base
                self.args.append(self.memory[position])
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

    def adjust_relative_base(self):
        if len(self.args) != 1:
            raise RuntimeError("Need arguments to jit")
        self.relative_base += self.args[0]
        self.args = []

    def _input(self):
        position = self.read()
        self.memory[position] = self.data_in.get()

        # print(f'writing {self.memory[position]} to {position}')
        self.args = []

    def output(self):
        while self.args:
            self.data_out.put(self.args.pop(0))
        # print(f'reading {self.memory[position]} from {position}')
        self.args = []

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

    def iterate(self):
        op = self.get_operation()
        # print(f'doing {op} with modes {self.mode}', end=' ')
        self.get_args()
        # print(f'args {self.args}')
        command = self.mapping[op]
        return command(self)

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
        return "".join(map(str, list(self.data_out.queue)))

    mapping = {
        1: add,
        2: multiply,
        3: _input,
        4: output,
        5: jit,
        6: jif,
        7: lt,
        8: eq,
        9: adjust_relative_base,
        99: halt,
    }

    num_args = {1: 2, 2: 2, 3: 0, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 1, 99: 0}


def process_input():
    file = "a.txt"
    with open(file) as f:
        data = f.readlines()
    data = [_.strip() for _ in data]
    return data


def get_input(data: str = None):
    if not data:
        data = process_input()[0]
    data = Memory(map(int, data.split(",")))
    return data


def solve(data=None, data_in=None):
    if data_in is None:
        data_in = []
    c = Computer(get_input(data))
    while data_in:
        c.data_in.put(data_in.pop(0))
    return c.run()


def main():
    print(solve(data_in=[1]))


if __name__ == "__main__":
    main()
