from __future__ import annotations

import importlib
import pprint
import re
from itertools import combinations
from typing import List
import numpy as np

from cinnamon_tools.point import Point, zero_point
Moon = getattr(importlib.import_module("12.a"), "Moon")

pp = pprint.PrettyPrinter(indent=4)
debug = False


def read_input():
    file = "input.txt"
    with open(file) as f:
        data = f.readlines()
    data = [_.strip() for _ in data]
    return data


def parse_input(data: str = None):
    if not data:
        data = read_input()
    data = [Moon(Point(*map(int, re.findall(r'-?\d+', d)))) for d in data]
    return data


def simulate(moons: List[Moon]):
    pairs = combinations(moons, 2)
    for a, b in pairs:
        a.apply_gravity(b)
    for m in moons:
        m.apply_velocity()


def find_loop(moons: List[Moon]):
    runs = 0
    simulate(moons)
    runs += 1
    while not all(map(lambda m: m.at_start, moons)):
        simulate(moons)
        runs += 1
    return runs


def solve(data=None):
    """
    Simulate the motion of the moons in time steps.
    Within each time step, first update the velocity of every moon by applying gravity.
    Then, once all moons' velocities have been updated,
    update the position of every moon by applying velocity.
    Time progresses by one step once all of the positions are updated.
    """
    moons = parse_input(data)
    x_moons = []
    y_moons = []
    z_moons = []
    for moon in moons:
        x_moons.append(Moon(Point(moon.position[0]), Point(moon.velocity[0])))
        y_moons.append(Moon(Point(moon.position[1]), Point(moon.velocity[1])))
        z_moons.append(Moon(Point(moon.position[2]), Point(moon.velocity[2])))
    x = find_loop(x_moons)
    y = find_loop(y_moons)
    z = find_loop(z_moons)
    return np.lcm(x, np.lcm(y, z))


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
