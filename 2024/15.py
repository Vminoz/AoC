"""--- Day 15: Warehouse Woes ---"""

from collections import deque

from common import do_part_on_input, logger
from common.maths import P2D
from common.visuals import p2d_sets_string

DIRECTIONS = {
    "^": (-1, 0),  # U
    "v": (1, 0),  # D
    "<": (0, -1),  # L
    ">": (0, 1),  # R
}
BOX = "□"
ROBOT = "ඞ"
WALL = "█"
BL = "┣"
BR = "┫"


def decorate(symbols: str) -> str:
    return (
        symbols.replace("#", WALL)
        .replace("O", BOX)
        .replace("@", ROBOT)
        .replace("[", BL)
        .replace("]", BR)
    )


def read_objects_and_moves(
    filename: str, widen: bool = False
) -> tuple[dict[P2D, str], str]:
    with open(filename) as f:
        symbols, moves = f.read().split("\n\n")

    if widen:
        symbols = (
            symbols.replace("#", "##")
            .replace(".", "..")
            .replace("O", "[]")
            .replace("@", "@.")
        )

    symbols = decorate(symbols)

    objects = {
        (i, j): c
        for i, row in enumerate(symbols.split("\n"))
        for j, c in enumerate(row)
        if c != "."
    }
    moves = moves.replace("\n", "")

    if logger.is_verbose:
        logger.m(p2d_sets_string(symbols=objects))
    return objects, moves


def gps_coord(p: P2D) -> int:
    return 100 * p[0] + p[1]


def update(objects: dict[P2D, str], robot: P2D, direction: P2D) -> P2D:
    new_rob = (robot[0] + direction[0], robot[1] + direction[1])

    new_box = new_rob
    while new_box in objects:
        if objects[new_box] == WALL:
            return robot
        new_box = (new_box[0] + direction[0], new_box[1] + direction[1])

    if new_box != robot:
        # just need to add a box at the end since robot will overwrite the first
        objects[new_box] = BOX

    objects[new_rob] = objects.pop(robot)
    return new_rob


def update_wide(objects: dict[P2D, str], robot: P2D, direction: P2D) -> P2D:
    di, dj = direction
    to_check = deque([robot])
    pushed = []
    # look ahead
    while to_check:
        p = to_check.popleft()
        if p in pushed:
            continue
        pushed.append(p)

        next_pos = (p[0] + di, p[1] + dj)
        if next_pos in objects:
            o = objects[next_pos]
            if o == WALL:
                return robot
            if dj == 0:  # vertical
                if o == BL:
                    to_check.append((p[0] + di, p[1] + 1))
                elif o == BR:
                    to_check.append((p[0] + di, p[1] - 1))
            to_check.append(next_pos)

    # go back and change
    while pushed:
        p = pushed.pop()
        objects[(p[0] + di, p[1] + dj)] = objects.pop(p)

    return (robot[0] + di, robot[1] + dj)


def sum_box_gps_coords(objects: dict[P2D, str]) -> int:
    return sum(gps_coord(p) for p, v in objects.items() if v in (BOX, BL))


def sum_gps_coords_after_moves(filename: str, widen: bool = False) -> int:
    objects, moves = read_objects_and_moves(filename, widen)
    robot = [k for k, v in objects.items() if v == ROBOT][0]

    for m in moves:
        robot = (
            update_wide(objects, robot, DIRECTIONS[m])
            if widen
            else update(objects, robot, DIRECTIONS[m])
        )
        if logger.is_verbose:
            logger.m(p2d_sets_string(symbols=objects) + m)

    return sum_box_gps_coords(objects)


def main():
    do_part_on_input(1, sum_gps_coords_after_moves)
    do_part_on_input(2, sum_gps_coords_after_moves, widen=True)


if __name__ == "__main__":
    main()
