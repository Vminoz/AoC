"""--- Day 10: Hoof It ---"""

from collections import deque
from typing import TypeAlias

from common import do_part, lines, logger, parse_input_with
from common.maths import P2D, neighbors_4
from common.visuals import p2d_sets_string

Topo: TypeAlias = dict[P2D, int]

SYMBOL_GRADIENT = "⊙·⠒⠦⠶⠷⠿⡿⣿⧊"


def parse_topography(filename: str) -> Topo:
    topo = {}
    for i, line in enumerate(lines(filename)):
        for j, c in enumerate(line.strip()):
            topo[i, j] = int(c)
    return topo


def sum_trail_scores(topo: Topo, rating: bool = False) -> int:
    starts = {(i, j) for i, j in topo if topo[i, j] == 0}
    res = 0
    for start in starts:
        score, positions = score_trail(start, topo, rating)
        if logger.is_verbose:
            show_map(topo, positions)
        res += score

    return res


def show_map(topo: Topo, positions: set[P2D]) -> None:
    logger.m(
        p2d_sets_string(
            positions,
            secondary_symbols={p: SYMBOL_GRADIENT[h] for p, h in topo.items()},
        )
    )


def score_trail(start_pos: P2D, topo: Topo, rating: bool) -> tuple[int, set[P2D]]:
    score = 0
    counted = set()
    q: deque[tuple[P2D, set[P2D]]] = deque([(start_pos, set())])
    trails = set()
    while q:
        p, visited = q.popleft()
        visited.add(p)

        if topo[p] == 9 and (rating or p not in counted):
            score += 1
            counted.add(p)
            trails |= visited
            continue

        for n in neighbors_4(p):
            if n in topo and topo[n] == topo[p] + 1:
                q.append((n, visited.copy()))
    return score, trails


def main():
    do_part(1, sum_trail_scores, parse_input_with(parse_topography))
    do_part(2, sum_trail_scores, parse_input_with(parse_topography), rating=True)


if __name__ == "__main__":
    main()
