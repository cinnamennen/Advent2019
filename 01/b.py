import pprint
import re
from typing import List

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    data = [int(d) for d in data]
    return data


def get_fuel(mass: int):
    to_add = (mass // 3) - 2
    if to_add > 0:
        additional = get_fuel(to_add)
        to_add += additional
    else:
        return 0
    return to_add


def solve(modules: List[int]) -> int:
    return sum(map(get_fuel, modules))


def main():
    print(solve(get_input()))


if __name__ == '__main__':
    main()
