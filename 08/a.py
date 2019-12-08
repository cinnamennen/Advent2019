from __future__ import annotations
import pprint
import re
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Dict, Union, Callable
from tqdm import trange
import networkx as nx

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = "a.txt"
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input(data: List[str] = None):
    if not data:
        data = process_input()[0]

    return list(map(int, data))


def solve(x, y, data=None) -> int:
    picture = get_input(data)
    pixel_count = x * y
    layers = [picture[i : i + pixel_count] for i in range(0, len(picture), pixel_count)]
    best = layers.pop(0)
    while layers:
        compare = layers.pop(0)
        if compare.count(0) < best.count(0):
            best = compare

    return best.count(1) * best.count(2)


def main():
    print(solve(25, 6))


if __name__ == "__main__":
    main()
