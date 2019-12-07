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


@dataclass
class Computer:
    data_in: Queue
    data_out: Queue
    memory: List[int]
    position: int = 0
    broken: bool = field(default=False, init=False)
    mode: List[int] = field(default_factory=list, init=False)
    args: List[int] = field(default_factory=list, init=False)

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
        self.memory[position] = self.data_in.get()

        # print(f'writing {self.memory[position]} to {position}')
        self.args = []

    def output(self):
        while self.args:
            self.data_out.put(self.args.pop(0))
        self.data_in.task_done()
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
        # return self.accumulated_output

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


def solve(var, data=None):
    ranges = permutations(var)
    best = -1
    for test in tqdm(ranges):
        output = soft_solve(data, test)
        if output > best:
            best = output

    return best


def soft_solve(data, settings: List[int]):
    old = Queue()

    first = True
    computers = []
    for setting in settings:
        new = Queue()
        old.put(setting)
        if first:
            old.put(0)
            first = False
        c = Computer(old, new, get_input(data))
        old = new
        computers.append(c)
    computers[-1].data_out = computers[0].data_in

    threads = [threading.Thread(target=c.run) for c in computers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return computers[-1].data_out.get()


def main():
    print(solve((5, 6, 7, 8, 9)))


if __name__ == "__main__":
    main()
