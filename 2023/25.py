import random
from dataclasses import dataclass
from itertools import count

from common import do_part_on_input, logger


@dataclass
class Graph:
    """Undirected graph with integer edge weights/duplicates"""

    edges: dict[tuple[str, str], int]

    def __post_init__(self):
        # Store two-way adjacency as a dict
        self.graph: dict[str, set[str]] = {}
        for e in self.edges:
            assert e[0] < e[1]
            self.graph.setdefault(e[0], set()).add(e[1])
            self.graph.setdefault(e[1], set()).add(e[0])

        # Prepare groups for later clustering
        self.groups = {k: {k} for k in self.graph}

    @classmethod
    def from_dict(cls, graph: dict[str, list[str]]) -> "Graph":
        """Build a graph from a dict like {"a": ["b", "c"]}"""
        adj = {}
        for u in graph:
            for v in graph[u]:
                adj[tuple(sorted((u, v)))] = 1
        return cls(adj)

    @classmethod
    def from_string(cls, graph: str) -> "Graph":
        """
        Build a graph from a string like:
        "<a>: <b> <c>\n<b>: <c>"
        """
        return cls.from_dict(
            {ln[0][:-1]: ln[1:] for ln in map(str.split, graph.split("\n"))}
        )

    def __len__(self) -> int:
        return len(self.graph)

    def n_edges(self) -> int:
        return sum(self.edges.values())

    def copy(self) -> "Graph":
        """Returns a copy of the graph, is a deepcopy if typing followed"""
        return Graph(self.edges.copy())

    def pick_edge(self) -> tuple[str, str]:
        return random.choices(
            list(self.edges.keys()),
            list(self.edges.values()),
        )[0]

    def contract_edge(self, edge: tuple[str, str]) -> None:
        self.edges.pop(edge)
        u, v = edge
        self.graph[u].remove(v)
        self.groups[u].update(self.groups.pop(v))
        v_neighbors = self.graph.pop(v) - {u}
        self.graph[u].update(v_neighbors)
        logger.d(v_neighbors)

        for n in v_neighbors:
            logger.d(n)
            self.graph[n] -= {v}
            ec = self.edges.pop(sorted_pair(v, n))
            self.graph[n].add(u)
            t = sorted_pair(u, n)
            self.edges[t] = self.edges.get(t, 0) + ec

    def karger_min_cut(self) -> tuple[int, ...]:
        """
        Return the edge count and the cluster sizes after Karger's algorithm
        - https://en.wikipedia.org/wiki/Karger%27s_algorithm
        """
        logger.v(self.graph)
        while len(self.graph) > 2:
            edge = self.pick_edge()
            logger.d(edge)
            self.contract_edge(edge)
        return self.n_edges(), *self.cluster_sizes()

    def cluster_sizes(self) -> list[int]:
        return [len(g) for g in self.groups.values()]


def sorted_pair(a, b):
    return (a, b) if a < b else (b, a)


def cut_3_group_size_checksum(filename: str, known_minimum: int = 3):
    graph = Graph.from_string(open(filename).read())
    logger.v(graph)
    edge_count = graph.n_edges()

    # Retry Karger's algorithm until we hit the known edge minimum
    # REALLY SLOW! Should use NCut with the unnormalized graph Laplacian
    for cnt in count():
        logger.v(f"Attempt #{cnt}")
        n_g = graph.copy()
        edge_count, s1, s2 = n_g.karger_min_cut()
        logger.v(f"→ {edge_count}")
        if edge_count == known_minimum:
            logger.i(f"Found {known_minimum} after {cnt + 1} attempts")
            return f"{s1 * s2} ({cnt + 1} attempts)"
    raise ValueError(f"Could not find {known_minimum}")


def main():
    do_part_on_input(1, cut_3_group_size_checksum)  # 569904 | 54
    # No part 2


if __name__ == "__main__":
    main()
