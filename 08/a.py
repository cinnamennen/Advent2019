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
        data = process_input()

    return data


def solve(x, y, data=None) -> int:
    layers = get_input(data)
    return layers


def main():
    print(solve(25, 6))


if __name__ == "__main__":
    main()
