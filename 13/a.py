from __future__ import annotations

import pprint
from dataclasses import dataclass
from enum import Enum

from cinnamon_tools.point import Point

from common.computer import computer_from_string

pp = pprint.PrettyPrinter(indent=4)
debug = False


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


@dataclass
class Tile:
    position: Point
    tile_id: TileType


def read_input():
    file = "input.txt"
    with open(file) as f:
        data = f.readlines()
    data = [_.strip() for _ in data]
    return data


def parse_input(data: str = None):
    if not data:
        data = read_input()[0]
    return data


def solve(data=None):
    program = parse_input(data)
    c = computer_from_string(program)
    a = c.run()
    tiles = []
    while not c.data_out.empty():
        tiles.append(Tile(Point(c.data_out.get(), c.data_out.get()), TileType(c.data_out.get())))
    return len([t for t in tiles if t.tile_id == TileType.BLOCK])


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
