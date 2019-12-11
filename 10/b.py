from __future__ import annotations

import pprint
from collections import deque
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
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if val == "#":
                stars.add(Point(x, y))

    return stars


def cart2pol(p: Point):
    rho = np.sqrt(p.x ** 2 + p.y ** 2)
    phi = np.arctan2(p.y, p.x) % (2 * np.pi)
    return Point(rho, phi)


def pol2cart(p: Point):
    x = round(p.x * np.cos(p.y))
    y = round(p.x * np.sin(p.y))
    return Point(x, y)


def solve(data=None) -> int:
    asteroids = get_input(data)
    best, coords = find_best_location(asteroids)
    field = deque(
        sorted(
            map(cart2pol, map(lambda q: q - coords, asteroids - {coords})),
            key=lambda p: (p.y, p.x),
        )
    )
    while field[0].y < (-90 * (np.pi / 180)) % (2 * np.pi):
        field.rotate(-1)

    # pp.pprint(field)
    # print(coords)
    destroyed_count = 0

    while destroyed_count < 200:
        destroyed = field.popleft()
        destroyed_count += 1
        # print(f'{destroyed_count}: {pol2cart(destroyed) + coords}')
        while field[0].y == destroyed.y:
            field.rotate(-1)
    p = pol2cart(destroyed) + coords
    # print(p)
    return int(p.x * 100 + p.y)


def find_best_location(asteroids):
    best = 0
    coords = Point(0, 0)
    for asteroid in tqdm(asteroids):
        count = len(
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
        if count > best:
            best = count
            coords = asteroid
    return best, coords


def main():
    print(solve())


if __name__ == "__main__":
    main()
