from __future__ import annotations

import pprint
from typing import List, Set

import numpy as np
from cinnamon_tools.point import Point
from tqdm import tqdm

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = "a.txt"
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input(data: List[str] = None) -> Set[Point]:
    if not data:
        data = process_input()

    stars = set()
    for x, row in enumerate(data):
        for y, val in enumerate(row):
            if val == "#":
                stars.add(Point(x, y))

    return stars


def solve(data=None) -> int:
    asteroids = get_input(data)
    relative = max(
        len(
            set(
                map(
                    lambda x: x.y,
                    map(
                        lambda p: Point(
                            np.sqrt(p.x ** 2 + p.y ** 2), np.arctan2(p.y, p.x)
                        ),
                        map(lambda q: q - asteroid, asteroids - {asteroid}),
                    ),
                )
            )
        )
        for asteroid in tqdm(asteroids)
    )
    return relative


def main():
    print(solve())


if __name__ == "__main__":
    main()
