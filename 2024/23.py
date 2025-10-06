"""--- Day 23: LAN Party ---"""

from collections import defaultdict
from typing import TypeAlias

from common import do_part_on_input, lines

Peers: TypeAlias = set[str]


def read_network(filename: str) -> dict[str, Peers]:
    g: defaultdict[str, Peers] = defaultdict(set)
    for line in lines(filename):
        left, right = line.rstrip().split("-")
        g[left].add(right)
        g[right].add(left)
    return g


def groups_of_3_with_t(filename: str) -> int:
    g = read_network(filename)
    return len(
        {
            "".join(sorted((node, p1, p2)))
            for node, peers in g.items()
            if node.startswith("t")
            for p1 in peers
            for p2 in peers
            if p2 in g[p1]
        }
    )


def find_lan(filename: str) -> str:
    g = read_network(filename)
    return find_largest_clique(g)


def find_largest_clique(graph: dict[str, Peers]) -> str:
    largest: list[str] = []
    for node, peers in graph.items():
        pl = list(peers)
        for i, p1 in enumerate(pl):
            clq = [node, p1]
            others = set(pl[i + 1 :]) & graph[p1]
            while others:
                o = others.pop()
                clq.append(o)
                others &= graph[o]
            if len(clq) > len(largest):
                largest = clq
    return ",".join(sorted(largest))


def main():
    do_part_on_input(1, groups_of_3_with_t)
    do_part_on_input(2, find_lan)


if __name__ == "__main__":
    main()
