from collections import defaultdict as DD
from collections import deque as DQ
from typing import Iterable, TypeAlias

from common import P2D, do_part_on_input, lines, logger
from common.visuals import p2d_sets_string

DIRECTIONS = {">": 1j, "v": 1, "<": -1j, "^": -1}
START_POS = 1j

logger.timestamp_lv = 2

WeightedGraph: TypeAlias = DD[complex, dict[complex, int]]


def to_p2d(complex_idx: complex) -> P2D:
    return (int(complex_idx.real), int(complex_idx.imag))


def to_p2ds(complex_idx: Iterable[complex]) -> set[P2D]:
    return {to_p2d(i) for i in complex_idx}


def reverse_map(d: dict[str, set[complex]]) -> dict[P2D, str]:
    return {t: k for k, v in d.items() for t in to_p2ds(v)}


def parse_map(filename: str) -> tuple[set[complex], dict[str, set[complex]], complex]:
    paths = set()
    slopes = {k: set() for k in DIRECTIONS}
    for i, line in enumerate(lines(filename)):
        for j, ch in enumerate(line):
            if ch == ".":
                paths.add(i + j * 1j)
            elif ch in DIRECTIONS:
                slopes[ch].add(i + j * 1j)
    end_pos = i + (j - 1) * 1j
    return paths, slopes, end_pos


def compress_map(
    paths: set[complex],
    slopes: dict[str, set[complex]],
    end_pos: complex,
) -> WeightedGraph:
    """Only keep crossroads and distances between them, prune dead ends"""
    graph = DD(dict)
    to_visit = DQ([(START_POS, 0 + 0j, START_POS, 0)])
    any_path = paths.union(*slopes.values())
    visited = set()
    while to_visit:
        source, p_pos, c_pos, dist = to_visit.pop()
        reachable = set()
        connected = 0
        dist += 1
        for d in DIRECTIONS:
            n_pos = c_pos + DIRECTIONS[d]
            if n_pos != p_pos and n_pos in any_path:
                connected += 1
                if n_pos in paths or n_pos in slopes[d]:
                    reachable.add(n_pos)
            if n_pos == end_pos:
                graph[source][n_pos] = dist

        is_node = connected > 1
        if is_node:
            graph[source][c_pos] = dist
            source = c_pos
            dist = 0

        for n_pos in reachable:
            if n_pos not in visited:
                to_visit.append((source, c_pos, n_pos, dist))

        if is_node and logger.level > 2:
            logger.d(source, c_pos, dist, reachable, to_visit)
            logger.m(
                p2d_sets_string(
                    to_p2ds(graph),
                    to_p2ds(visited),
                    reverse_map(slopes) | {to_p2d(c_pos): "*"},
                )
            )

        if not is_node:
            visited.add(c_pos)

    return graph


def dfs_longest_path(
    graph: WeightedGraph,
    target: complex,
    source: complex = START_POS,
) -> tuple[int, list[complex]]:
    to_visit = [(source, [source], 0)]
    paths_to_target = {}
    while to_visit:
        c_pos, c_path, c_dist = to_visit.pop()
        if c_pos == target:
            paths_to_target[c_dist] = c_path
            continue

        for n_pos, dist in graph[c_pos].items():
            if n_pos in c_path:
                continue

            n_dist = c_dist + dist
            n_path = c_path + [n_pos]

            to_visit.append((n_pos, n_path, n_dist))
    return max(paths_to_target.items(), key=lambda x: x[0])


def reversify_edges(graph: WeightedGraph) -> None:
    for node in list(graph):
        for dest, dist in graph[node].items():
            graph[dest][node] = dist


def it_feels_like_we_only_go_forwards(
    graph: WeightedGraph,
    source: complex = START_POS,
):
    to_visit = [source]
    while to_visit:
        t_junctions = []
        for node in to_visit:
            for dest in graph[node]:
                if len(graph[dest]) == 3:
                    graph[dest].pop(node, None)
                    t_junctions.append(dest)
        to_visit = t_junctions


def print_graph_maybe(graph: WeightedGraph):
    if logger.level > 2:
        logger.v()
        logger.d("\n".join(f"{k:<10}: {v}" for k, v in graph.items()))


def hike_long(filename: str, can_climb: bool = False) -> int:
    paths, slopes, end_pos = parse_map(filename)
    logger.v("parsed")
    graph = compress_map(paths, slopes, end_pos)
    logger.v("compressed")

    if can_climb:
        reversify_edges(graph)
        print_graph_maybe(graph)
        it_feels_like_we_only_go_forwards(graph)
    print_graph_maybe(graph)

    cmax, path = dfs_longest_path(graph, end_pos)

    if logger.is_verbose:
        from string import ascii_letters as al

        logger.m(
            p2d_sets_string(
                set(),
                to_p2ds(paths),
                reverse_map(slopes) | {to_p2d(p): s for p, s in zip(path, al)},
            )
        )

    return cmax


def main():
    do_part_on_input(1, hike_long)
    do_part_on_input(2, hike_long, can_climb=True)


if __name__ == "__main__":
    main()
