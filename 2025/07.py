"""--- Day 7: Laboratories ---"""

from collections import Counter

from common import do_part_on_input, lines, logger
from common.maths import P2D
from common.visuals import p2d_sets_string


def parse_beam_box(filename: str) -> tuple[set[P2D], P2D]:
    splitters = set()
    start = None
    for i, line in enumerate(lines(filename)):
        for j, c in enumerate(line):
            if c == "S":
                start = (i, j)
            elif c == "^":
                splitters.add((i, j))
    if not start:
        raise ValueError("No start found")
    return splitters, start


def down(p: P2D) -> P2D:
    return p[0] + 1, p[1]


def split(p: P2D) -> tuple[P2D, P2D]:
    return (p[0], p[1] - 1), (p[0], p[1] + 1)


def step(splitters: set[P2D], beams: Counter[P2D]) -> tuple[int, Counter[P2D]]:
    n_splits = 0
    next_beams: Counter[P2D] = Counter()
    for b, n in beams.items():
        below = down(b)
        if below in splitters:
            n_splits += 1
            left, right = split(below)
            next_beams[left] += n
            next_beams[right] += n
        else:
            next_beams[below] += n
    return n_splits, next_beams


def count_beams(filename: str, splits: bool = True) -> int:
    splitters, start = parse_beam_box(filename)
    beams = Counter((start,))
    n_splits = 0
    bottom = max(splitters, key=lambda x: x[0])[0]
    for _ in range(bottom):
        logger.d(beams)
        new_splits, beams = step(splitters, beams)
        n_splits += new_splits
        if logger.is_verbose and splits:
            logger.m(
                p2d_sets_string(
                    symbols={p: "│" for p in beams},
                    secondary_symbols={start: "S", **{p: "^" for p in splitters}},
                )
                + str(n_splits)
            )
    return n_splits if splits else beams.total()


def main():
    do_part_on_input(1, count_beams)
    do_part_on_input(2, count_beams, splits=False)


if __name__ == "__main__":
    main()
