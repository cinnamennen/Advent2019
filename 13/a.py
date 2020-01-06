from __future__ import annotations

import pprint
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from cinnamon_tools.point import Point
from common.computer import computer_from_string, Computer

pp = pprint.PrettyPrinter(indent=4)
debug = False


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


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
    c: Computer = computer_from_string(program)
    threading.Thread(target=c.run).start()
    tiles: Dict[Point, TileType] = {}
    while not (c.broken and c.data_out.empty()):
        x, y, t = c.data_out.get(), c.data_out.get(), c.data_out.get()
        tiles[Point(x, y)] = TileType(t)
    return len(list(filter(lambda tile: tile == TileType.BLOCK, tiles.values())))


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
