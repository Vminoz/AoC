"""--- Day 14: Restroom Redoubt ---"""

from collections import Counter
from dataclasses import dataclass
from functools import reduce
from operator import mul

from common import do_part_on_input, lines, logger
from common.input_parsing import USE_SMALL_FILE, re_4d
from common.maths import P2D, BBox, neighbors_4
from common.visuals import p2d_sets_string

if USE_SMALL_FILE:
    BBOX = BBox(lower=(0, 0), upper=(6, 10))
else:
    BBOX = BBox(lower=(0, 0), upper=(102, 100))

T = 100


@dataclass
class Robot:
    j: int
    i: int
    dj: int
    di: int

    @property
    def pos(self) -> P2D:
        return (self.i, self.j)

    def step(self, bbox: BBox) -> None:
        self.i += self.di
        self.j += self.dj

        if self.i < bbox.lower[0]:
            self.i += bbox.ispan[0]
        elif self.i > bbox.upper[0]:
            self.i -= bbox.ispan[0]

        if self.j < bbox.lower[1]:
            self.j += bbox.ispan[1]
        elif self.j > bbox.upper[1]:
            self.j -= bbox.ispan[1]


def safety_factor_after_t(filename: str) -> int:
    robots = [Robot(*re_4d(line)) for line in lines(filename)]

    if logger.is_verbose:
        show_robots(robots)

    for t in range(T):
        for r in robots:
            logger.d("before", r)
            r.step(BBOX)
            logger.d("after", r)

        if logger.is_verbose:
            show_robots(robots, t + 1)

    return get_safety_factor(robots)


def get_safety_factor(robots: list[Robot]) -> int:
    counts = [0, 0, 0, 0]
    max_i, max_j = BBOX.upper[0], BBOX.upper[1]
    mid_i, mid_j = max_i // 2, max_j // 2
    quadrants = (
        BBox((0, 0), (mid_i - 1, mid_j - 1)),  # UL
        BBox((0, mid_j + 1), (mid_i - 1, max_j)),  # UR
        BBox((mid_i + 1, 0), (max_i, mid_j - 1)),  # LL
        BBox((mid_i + 1, mid_j + 1), (max_i, max_j)),  # LR
    )
    for r in robots:
        for i, q in enumerate(quadrants):
            if r.pos in q:
                counts[i] += 1
    return reduce(mul, counts)


def show_robots(robots: list[Robot], t: int = 0):
    c = {k: str(v) for k, v in Counter(r.pos for r in robots).items()}
    logger.m(p2d_sets_string(symbols=c, bounding_box=BBOX) + str(t))


def look_for_picture(filename: str) -> int:
    robots = [Robot(*re_4d(line)) for line in lines(filename)]
    most_robots = len(robots) // 4  # most, 25%. same same
    c = 0
    while True:
        c += 1
        positions = set()
        for r in robots:
            r.step(BBOX)
            positions.add(r.pos)

        if largest_connected_component_size(positions) > most_robots:
            if logger.is_verbose:
                show_robots(robots, c)
            return c


def largest_connected_component_size(positions: set[P2D]) -> int:
    largest = 0
    while positions:
        p = positions.pop()
        connected = {p}
        size = 0
        while connected:
            size += 1
            p = connected.pop()
            nbs = {nb for nb in neighbors_4(p) if nb in positions}
            positions -= nbs
            connected |= nbs
        largest = max(largest, size)
    return largest


def main():
    do_part_on_input(1, safety_factor_after_t)
    do_part_on_input(2, look_for_picture)


if __name__ == "__main__":
    main()
