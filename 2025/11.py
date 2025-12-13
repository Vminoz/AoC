"""--- Day 11: Reactor ---"""

from functools import cache
from typing import TypeAlias

from common import do_part_on_input, lines, logger

Graph: TypeAlias = dict[str, list[str]]


def parse_dag(filename: str) -> Graph:
    dag = {}
    for line in lines(filename):
        parts = line.strip().split()
        dag[parts[0].rstrip(":")] = parts[1:]
    return dag


def get_paths(g: Graph, src: str, dst: str) -> list[list[str]]:
    if src == dst:
        return [[src]]
    paths = []
    for neighbor in g.get(src, []):
        for path in get_paths(g, neighbor, dst):
            paths.append([src] + path)
    return paths


def count_paths(g: Graph, src: str, dst: str):
    @cache
    def dfs(current: str):
        if current == dst:
            return 1
        downstream = g.get(current)
        if not downstream:
            return 0
        return sum(dfs(n) for n in downstream)

    return dfs(src)


def part1(filename: str) -> int:
    dag = parse_dag(filename)
    paths = get_paths(dag, "you", "out")
    logger.v(paths)
    return len(paths)


def part2(filename: str) -> int:
    dag = parse_dag(filename)
    # Assumption: fft is upstream of dac
    nodes = ["svr", "fft", "dac", "out"]
    num_paths = 1
    for i, start in enumerate(nodes[:-1]):
        dest = nodes[i + 1]
        num_part_paths = count_paths(dag, start, dest)
        logger.v(start, " → ", dest, "\t", num_part_paths)
        num_paths *= num_part_paths
    return num_paths


def main():
    do_part_on_input(1, part1)
    do_part_on_input(2, part2)


if __name__ == "__main__":
    main()
