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


def pre_raster(x, y, data=None) -> List[List[int]]:
    layers = get_layers(x, y, data)

    raster = [[] for _ in range(x * y)]
    for layer in layers:
        for index, pixel in enumerate(layer):
            raster[index].append(pixel)
    return raster


def get_layers(x, y, data=None) -> List[List[int]]:
    picture = get_input(data)
    pixel_count = x * y
    layers = [picture[i: i + pixel_count] for i in range(0, len(picture), pixel_count)]
    return layers


def soft_solve(x, y, data=None) -> List[int]:
    raster = pre_raster(x, y, data)
    raster = list(map(lambda x: list(filter(lambda y: y != 2, x)), raster))  # Strip out transparent pixels

    image = [r[0] if r else None for r in raster]

    return image


def solve(x, y):
    picture = soft_solve(x, y)
    mapping = {
        1: '█',
        0: ' ',
        None: '░'
    }
    picture = [mapping[p] for p in picture]
    image = []
    while picture:
        temp = []
        for _ in range(x):
            temp.append(picture.pop(0))

        image.append(''.join(temp))
    for row in image:
        print(row)


def main():
    solve(25, 6)


if __name__ == "__main__":
    main()
