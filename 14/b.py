from __future__ import annotations

import math
import pprint
from collections import defaultdict
from dataclasses import dataclass, field
from queue import SimpleQueue
from typing import Dict, List

pp = pprint.PrettyPrinter(indent=4)
debug = False


@dataclass
class Component:
    substance: str
    amount: int

    def __mul__(self, other):
        return Component(self.substance, self.amount * other)

    def __rmul__(self, other):
        return self.__mul__(other)


@dataclass
class Recipe:
    result: Component
    ingredients: List[Component]
    extra: List[Component] = field(default_factory=list)


def read_input():
    file = "input.txt"
    with open(file) as f:
        return f.readlines()


def parse_recipe(r: str):
    i, o = r.split(" => ")
    output_amount, output_item = o.split()
    output_amount = int(output_amount)
    xx = list(Component(w.split()[1], int(w.split()[0])) for w in i.split(", "))
    return Recipe(Component(output_item, output_amount), xx)


def parse_input(data: str = None) -> Dict[str, Recipe]:
    if not data:
        data = read_input()
    else:
        data = data.splitlines()
    data = [_.strip() for _ in data]
    return {r.result.substance: r for r in map(parse_recipe, data)}


def get_cost(work: SimpleQueue, recipe_book: Dict[str, Recipe], extra: Dict[str, int]) -> int:
    ore_used = 0

    while not work.empty():
        to_make: Component = work.get()

        # Ore is infinite, we can just use it
        if to_make.substance == "ORE":
            ore_used += to_make.amount
            continue

        # Use up anything we already have
        usable = min(extra[to_make.substance], to_make.amount)
        to_make.amount -= usable
        extra[to_make.substance] -= usable

        # Dont need to craft it if you dont need it
        if to_make.amount == 0:
            continue

        recipe = recipe_book[to_make.substance]

        scaling_factor = math.ceil(to_make.amount / recipe.result.amount)

        for ingredient in recipe.ingredients:
            work.put(scaling_factor * ingredient)
        leftover = (scaling_factor * recipe.result.amount) - to_make.amount
        extra[to_make.substance] += leftover

    return ore_used


def solve(data=None):
    ore_available = 1000000000000
    works = 1
    too_high = ore_available
    recipes = parse_input(data)

    while (too_high - works) > 1:
        to_check = works + ((too_high - works) // 2)
        cost = soft_solve(recipes, to_check)
        if cost > ore_available:
            too_high = to_check
        else:
            works = to_check

    return works


def soft_solve(recipes, amount):
    work = SimpleQueue()
    work.put(Component("FUEL", amount))
    extra: Dict[str, int] = defaultdict(int)
    cost = get_cost(work, recipes, extra)
    return cost


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
