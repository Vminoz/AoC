"""--- Day 8: Resonant Collinearity ---"""

from collections import defaultdict
from itertools import combinations

from common import P2D, do_part, lines, logger, parse_input_with
from common.maths import BBox
from common.visuals import p2d_sets_string


def parse_antennas(filename: str) -> tuple[dict[P2D, str], BBox]:
    antennas = {}
    i, j = 0, 0
    for i, line in enumerate(lines(filename)):
        for j, c in enumerate(line):
            if c not in ".\n":
                antennas[(i, j)] = c
    if not (i and j):
        raise ValueError("Nothing was parsed")
    bbox = BBox((0, 0), (i, j))

    if logger.is_verbose:
        logger.v("Antennas:")
        logger.m(p2d_sets_string(symbols=antennas, bounding_box=bbox))

    return antennas, bbox


def group_positions_by_label(positions: dict[P2D, str]) -> dict[str, list[P2D]]:
    labels = defaultdict(list)
    for k, v in positions.items():
        labels[v].append(k)
    return labels


def count_antinodes(
    antennas: dict[P2D, str],
    bbox: BBox,
    propagate: bool = False,
) -> int:
    antennas_by_type = group_positions_by_label(antennas)
    antinodes = set()
    for antenna_type, positions in antennas_by_type.items():
        antinodes_ant_type = (
            get_antinodes_propagated(positions, bbox)
            if propagate
            else get_antinodes(positions)
        )
        for i, j in antinodes_ant_type:
            if (i, j) in bbox:
                antinodes.add((i, j))
        if logger.is_verbose:
            logger.m(
                f"{antenna_type}\n"
                + p2d_sets_string(
                    antinodes_ant_type,
                    antinodes,
                    secondary_symbols=antennas,
                    bounding_box=bbox,
                )
            )

    return len(antinodes)


def get_antinodes(antennas: list[P2D]) -> set[P2D]:
    """Antinodes appear for each antenna pair (a1,a2) at 2a1-a2 and 2a2-a1"""
    antinodes = set()
    for a1, a2 in combinations(antennas, 2):
        antinodes.add((2 * a1[0] - a2[0], 2 * a1[1] - a2[1]))
        antinodes.add((2 * a2[0] - a1[0], 2 * a2[1] - a1[1]))
    return antinodes


def get_antinodes_propagated(antennas: list[P2D], bbox: BBox) -> set[P2D]:
    """get_antinodes, but the the antinodes repeat until we're outside the bbox"""
    antinodes = set()
    for a1, a2 in combinations(antennas, 2):
        # antinodes at the antennas
        antinodes.add(a1)
        antinodes.add(a2)
        d = (a2[0] - a1[0], a2[1] - a1[1])
        # away from a1 (-d)
        node = (a1[0] - d[0], a1[1] - d[1])
        while node in bbox:
            antinodes.add(node)
            node = (node[0] - d[0], node[1] - d[1])
        # away from a2 (+d)
        node = (a2[0] + d[0], a2[1] + d[1])
        while node in bbox:
            antinodes.add(node)
            node = (node[0] + d[0], node[1] + d[1])
    return antinodes


def main():
    antennas, bbox = parse_input_with(parse_antennas)
    do_part(1, count_antinodes, antennas, bbox)
    do_part(2, count_antinodes, antennas, bbox, propagate=True)


if __name__ == "__main__":
    main()
