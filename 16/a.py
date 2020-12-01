import itertools
import pprint
from typing import List

from tqdm import trange

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


def solve(data=None):
    data = parse_input(data)
    for i in trange(100):
        data = get_phase(data, i + 1)
    return data[:8]


def main():
    print(solve())


def get_phase(input: str, phase: int) -> str:
    signal: list[int] = list(map(int, input))
    rv: list[int] = [get_digit(signal, phase + 1) for phase in range(len(signal))]
    return "".join(map(str, rv))


def get_pattern(phase: int) -> list[int]:
    return [
        item for sublist in [phase * [x] for x in [0, 1, 0, -1]] for item in sublist
    ]


def get_digit(signal: list[int], phase: int) -> int:
    repeating_generator = itertools.cycle(get_pattern(phase))
    next(repeating_generator)
    return abs(sum([v * next(repeating_generator) for v in signal])) % 10


if __name__ == "__main__":
    main()
