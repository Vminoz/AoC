from pathlib import Path
from typing import TypeAlias

from common import P2D, do_part_on_input, logger, tuple_ranges
from common.maths import shoelace_area
from common.visuals import make_polygon_svg, p2d_sets_string

Plan: TypeAlias = list[tuple[int, int, int]]
DIRECTIONS = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}
DIRCODE = {"0": (0, 1), "1": (1, 0), "2": (0, -1), "3": (-1, 0)}


def neighbors(i: int, j: int):
    return [(i + di, j + dj) for di, dj in DIRECTIONS.values()]


def lagoon_size(filename: str):
    plan = read_plan(filename)
    dug = dig(plan)
    if logger.level > 1:
        logger.m("Hole dug", True)
    filled = fill_hole(dug)
    if logger.level > 1:
        logger.m(p2d_sets_string(dug, filled))
    return len(dug) + len(filled)


def shoelace_lagoon(filename: str):
    plan = read_plan(filename, True)
    vertices, perimeter = thoughtful_dig(plan)
    if logger.level > 1:
        logger.m("Hole 【dug】", True)
        make_polygon_svg(vertices, file=Path(__file__).parent / "vis" / "18.svg")
    area = shoelace_area(vertices)

    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return area + 1 + perimeter // 2


def thoughtful_dig(plan: Plan) -> tuple[list[P2D], int]:
    perimeter = 0
    verts = [(0, 0)]
    for di, dj, step in plan:
        v = verts[-1]
        perimeter += step
        verts.append((v[0] + di * step, v[1] + dj * step))
    return verts, perimeter


def read_plan(filename: str, hex: bool = False) -> Plan:
    raw_plan = [line.split() for line in open(filename).read().split("\n")]
    plan = []
    while raw_plan:
        d, cnt, h = raw_plan.pop()
        if hex:
            h = h.strip("(#)")
            di, dj = DIRCODE[h[-1]]
            cnt = int(h[:-1], 16)
            logger.log(3, (di, dj), cnt)
        else:
            di, dj = DIRECTIONS[d]
            cnt = int(cnt)
        plan.append((di, dj, cnt))
    return plan


def fill_hole(dug: set[P2D]):
    i, j = enter_hole(dug)
    filled = {(i, j)}
    nbs = neighbors(i, j)
    its = 0
    while nbs:
        i, j = nbs.pop()
        if (i, j) in dug or (i, j) in filled:
            continue
        filled.add((i, j))
        nbs.extend(neighbors(i, j))
        if not its % 1_000_000:
            logger.v(its, len(nbs))
        its += 1
    return filled


def dig(plan: Plan):
    dug = {(0, 0)}
    i, j = 0, 0
    while plan:
        di, dj, cnt = plan.pop()
        for _ in range(int(cnt)):
            i += di
            j += dj
            dug.add((i, j))
    return dug


def enter_hole(dug: set[P2D]) -> P2D:
    # Will break if meeting a ] or [ shape 😎
    ri, rj = tuple_ranges(dug)
    i, j = ri.start - 1, (rj.stop + rj.start) // 2
    while (i, j) not in dug:
        i += 1
    while (i, j) in dug:
        i += 1
    return i, j


def main():
    do_part_on_input(1, lagoon_size)
    do_part_on_input(2, shoelace_lagoon)


if __name__ == "__main__":
    main()
