from __future__ import annotations
import pprint
import re
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Dict, Union, Callable, Tuple, Set

from cinnamon_tools.point import Point, zero_point, directions
from tqdm import trange

pp = pprint.PrettyPrinter(indent=4)


def process_input() -> List[str]:
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input(data: List[str] = None):
    if not data:
        data = process_input()
    data = [x.split('-') for x in data]
    data = data[0]
    data = list(map(int, data))

    return data


def test(password: str) -> bool:
    pat = re.compile(r'(\d)(\1+)')
    matches = re.findall(pat, password)
    if not matches or not any(map(lambda x: len(x[1]) == 1, matches)):
        return False
    orig = list(map(int, list(password)))
    if orig != sorted(orig):
        return False

    return True


def solve(data: List[str] = None) -> int:
    start, stop = get_input(data)
    counter = 0
    for p in trange(start + 1, stop + 1):
        if test(str(p)):
            counter += 1

    return counter


def main():
    print(solve())


if __name__ == '__main__':
    main()
