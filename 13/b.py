from __future__ import annotations

import pprint
from enum import Enum
from queue import Queue
from threading import Thread

from common.computer import computer_from_string, Computer

pp = pprint.PrettyPrinter(indent=4)
debug = False


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Joystick(Enum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


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


def update_tiles(c: Computer, paddle: Queue, ball: Queue, output: Queue):
    score = 0
    while not (c.broken and c.data_out.empty()):
        x, y, t = c.data_out.get(), c.data_out.get(), c.data_out.get()
        if x == -1 and y == 0:
            score = t
            continue
        else:
            tile = TileType(t)
            if tile == TileType.PADDLE:
                paddle.put(x)
            elif tile == TileType.BALL:
                ball.put(x)
            else:
                continue

    output.put(score)


def move_paddle(c: Computer, paddle: Queue, ball: Queue):
    while not c.broken:
        p = paddle.get()
        b = ball.get()
        if b == p:
            c.data_in.put(Joystick.NEUTRAL.value)
            paddle.put(p)
        elif b > p:
            c.data_in.put(Joystick.RIGHT.value)
        else:
            c.data_in.put(Joystick.LEFT.value)


def solve(data=None):
    program = parse_input(data)
    c: Computer = computer_from_string(program)
    c.memory[0] = 2
    Thread(target=c.run).start()
    paddle = Queue()
    ball = Queue()
    output = Queue()
    Thread(target=update_tiles, args=(c, paddle, ball, output)).start()
    Thread(target=move_paddle, args=(c, paddle, ball)).start()
    return output.get()


def main():
    answer = solve()
    print(answer)


if __name__ == "__main__":
    main()
