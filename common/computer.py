from dataclasses import dataclass, field
from typing import List
from queue import Queue

debug = False


class ArgumentError(RuntimeError):
    pass


class Memory(list):
    def __getitem__(self, key):
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]
        if key < 0:
            raise IndexError
        try:
            return super().__getitem__(key)
        except IndexError:
            missing = key - (len(self) - 1)
            self += [0] * missing
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key < 0:
            raise IndexError
        try:
            return super().__setitem__(key, value)
        except IndexError:
            missing = key - (len(self) - 1)
            self += [0] * missing
            return super().__setitem__(key, value)


@dataclass
class Computer:
    memory: Memory
    position: int = 0
    relative_base: int = 0
    mem_mode: int = -1
    doing_input: bool = field(default=False, init=False)
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
        temp = self.mode.pop()
        while self.mode:
            self.args.append(self.get_arg(self.mode.pop(0), self.read()))

        if not self.doing_input:
            self.args.append(self.get_arg(temp, self.read()))
        else:
            self.doing_input = False
            self.args.append(self.get_add(temp, self.read()))

    def get_add(self, mode, position):
        if mode == 0:
            return position
        elif mode == 1:
            raise RuntimeError(f"Cannot write to an immediate value")
        elif mode == 2:
            return position + self.relative_base
        else:
            raise RuntimeError(f"{mode} is not a valid mode")

    def get_arg(self, mode, position):
        if mode == 0:
            return self.memory[position]
        elif mode == 1:
            return position
        elif mode == 2:
            position += self.relative_base
            return self.memory[position]
        else:
            raise RuntimeError(f"{mode} is not a valid mode")

    def add(self):
        if len(self.args) != 3:
            raise ArgumentError
        self.memory[self.args.pop()] = self.args.pop(0) + self.args.pop(0)
        # print(f'writing to {position}, {self.memory[position]}')

    def multiply(self):
        if len(self.args) != 3:
            raise ArgumentError
        self.memory[self.args.pop()] = self.args.pop(0) * self.args.pop(0)
        # print(f'writing to {position}, {self.memory[position]}')

    def halt(self):
        if len(self.args) != 0:
            raise ArgumentError
        if debug:
            print("===STOPPING===")
        self.broken = True

    def adjust_relative_base(self):
        if len(self.args) != 1:
            raise ArgumentError
        self.relative_base += self.args.pop(0)
        # print(f'set relative base to {self.relative_base}')

    def _input(self):
        if len(self.args) != 1:
            raise ArgumentError
        self.memory[self.args.pop()] = self.data_in.get()

        # print(f'reading {self.memory[self.args[0]]} to {self.args[0]}')

    def output(self):
        if len(self.args) != 1:
            raise ArgumentError
        self.data_out.put(self.args.pop())

        # print(f'writing {self.memory[position]} from {position}')

    def jit(self):
        if len(self.args) != 2:
            raise ArgumentError
        to_jump = self.args.pop()
        if self.args.pop(0) != 0:
            # print(f'jumping to {self.args[1]} because {self.args[0]} != {0}')
            self.position = to_jump

    def jif(self):
        if len(self.args) != 2:
            raise ArgumentError
        to_jump = self.args.pop()
        if self.args.pop(0) == 0:
            # print(f'jumping to {self.args[1]} because {self.args[0]} != {0}')
            self.position = to_jump

    def lt(self):
        if len(self.args) != 3:
            raise ArgumentError

        self.memory[self.args.pop()] = 1 if self.args.pop(0) < self.args.pop(0) else 0

    def eq(self):
        if len(self.args) != 3:
            raise ArgumentError
        self.memory[self.args.pop()] = 1 if self.args.pop(0) == self.args.pop(0) else 0

    def iterate(self):
        op = self.get_operation()
        if op not in [4, 5, 6, 9, 99]:
            self.doing_input = True
        if debug:
            print(f"doing {self.mapping[op].__name__} with modes {self.mode}", end=" ")
        if op not in [99]:
            self.get_args()
        if debug:
            print(f"args {self.args}")
        command = self.mapping[op]
        val = command(self)
        assert len(self.args) == 0
        return val

    def get_operation(self) -> int:
        op_code = self.read()
        if debug:
            print(
                f"opcode was {op_code} with memory {self.memory[self.position:self.position + 4]} offset "
                f"{self.relative_base}"
            )
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
        return "\n".join(map(str, list(self.data_out.queue)))

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

    num_args = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}


def computer_from_string(s: str) -> Computer:
    return Computer(Memory(map(int, s.split(","))))
