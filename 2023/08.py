from itertools import cycle
from math import lcm
from typing import Iterator

from common import do_part, logger, parse_input_with


def read_map(filename: str):
    seq, graph = map(str.strip, open(filename).read().split("\n\n"))
    graph = parse_graph(graph.split("\n"))
    seq = cycle(seq)
    return seq, graph


def parse_graph(
    node_list: list[str],
    sep: str = " = ",
    edge_sep: str = ", ",
    pad: int = 1,
) -> dict[str, tuple[str, str]]:
    graph = {}
    for node in node_list:
        v, e = node.split(sep)
        e = e[pad:-pad].split(edge_sep)
        graph[v] = e
    return graph


def a_to_z(
    seq: Iterator,
    graph: dict[str, tuple[str, str]],
    st: str = "AAA",
    tgt: str = "ZZZ",
) -> int:
    node = st
    steps = 0
    while not node.endswith(tgt):
        steps += 1
        logger.v(steps)
        d = next(seq)
        logger.v(node, d)
        node = graph[node][d == "R"]
    return steps


def p2(seq, graph):
    return lcm(*(a_to_z(seq, graph, n, "Z") for n in graph if n[-1] == "A"))


def main():
    seq, graph = parse_input_with(read_map)
    do_part(1, a_to_z, seq, graph)
    do_part(2, p2, seq, graph)


if __name__ == "__main__":
    main()
