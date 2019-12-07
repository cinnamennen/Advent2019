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

    data = [d.split(")") for d in data]

    G = nx.Graph()
    for b, a in data:
        G.add_edge(a, b)
    return G


def solve(data=None) -> int:
    graph = get_input(data)
    # print(graph.nodes)
    distance = nx.shortest_path_length(graph, "SAN", "YOU")

    return distance - 2


def main():
    print(solve())


if __name__ == "__main__":
    main()
