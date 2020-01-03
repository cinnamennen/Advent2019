from __future__ import annotations
import pprint
import re
from dataclasses import dataclass
from itertools import combinations
from typing import List

from cinnamon_tools.point import Point, zero_point

pp = pprint.PrettyPrinter(indent=4)
debug = False


@dataclass
class Moon:
    position: Point
    velocity: Point = zero_point(3)

    def apply_gravity(self, other: Moon):
        """
        To apply gravity, consider every pair of moons.
        On each axis (x, y, and z), the velocity of each moon
        changes by exactly +1 or -1 to pull the moons together.

        For example,
        if Ganymede has an x position of 3,
        and Callisto has a x position of 5,
        then Ganymede's x velocity changes by +1 (because 5 > 3)
        and Callisto's x velocity changes by -1 (because 3 < 5).
        However, if the positions on a given axis are the same,
        the velocity on that axis does not change for that pair of moons.
        """
        difference = self.position - other.position
        normalized = Point(*map(lambda p: 1 if p > 0 else -1 if p < 0 else 0, difference))
        other.velocity += normalized
        self.velocity += normalized * -1

    def apply_velocity(self):
        self.position += self.velocity

    @property
    def potential_energy(self) -> int:
        return sum(map(abs, self.position.values))

    @property
    def kinetic_energy(self) -> int:
        return sum(map(abs, self.velocity.values))

    @property
    def total_energy(self) -> int:
        return self.kinetic_energy * self.potential_energy


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


def solve(data=None, steps=0):
    """
    Simulate the motion of the moons in time steps.
    Within each time step, first update the velocity of every moon by applying gravity.
    Then, once all moons' velocities have been updated,
    update the position of every moon by applying velocity.
    Time progresses by one step once all of the positions are updated.
    """
    moons = parse_input(data)
    for _ in range(steps):
        simulate(moons)

    return sum(map(lambda m: m.total_energy, moons))


def main():
    answer = solve(steps=1000)
    print(answer)


if __name__ == "__main__":
    main()
