from __future__ import annotations

import math
import pprint
from collections import defaultdict
from dataclasses import dataclass, field
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


def use_extra_bits(extra: Dict[str, int], need: List[Component]):
    for component in need:
        if component.substance in extra:
            usable = min(extra[component.substance], component.amount)
            component.amount -= usable
            extra[component.substance] -= usable

            if extra[component.substance] == 0:
                del extra[component.substance]
    [need.remove(c) for c in need if c.amount < 1]


def get_cost(
    substance: str,
    amount: int,
    recipe_book: Dict[str, Recipe],
    extra: Dict[str, int],
) -> List[Component]:
    if substance == "ORE":
        return [Component("ORE", amount)]
    print(f'getting the cost for {amount} {substance}')
    recipe = recipe_book[substance]
    scaling_factor = math.ceil(amount / recipe.result.amount)
    need: List[Component] = list(map(lambda c: c * scaling_factor, recipe.ingredients))

    # Go through and use anything we've already made
    use_extra_bits(extra, need)

    need = [
        item
        for component in need
        for item in get_cost(component.substance, component.amount, recipe_book, extra)
    ]

    # Simplify the craft by combining the same requirements
    simplified = defaultdict(int)
    for component in need:
        simplified[component.substance] += component.amount

    need = [Component(sub, amt) for sub, amt in simplified.items()]
    amount_extra = (recipe.result.amount * scaling_factor) - amount
    if amount_extra > 0:
        extra[substance] = amount_extra

    return need


def solve(data=None):
    recipes = parse_input(data)
    cost = get_cost("FUEL", 1, recipes, {})
    if len(cost) != 1 or cost[0].substance != 'ORE':
        print('calculation error', cost)
    return cost[0].amount


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
