# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "graphviz==0.21",
# ]
# ///

from functools import cache
from typing import TypeAlias

import graphviz

Graph: TypeAlias = dict[str, list[str]]


def generic_pretty_graph(
    graph: dict[str, list[str]],
    highlight: dict[str, str] | None = None,
    highlight_edges: dict[tuple[str, str], str] | None = None,
    filename: str = "graph",
    directed=True,
    engine="dot",
    arrowheads="none",
):
    """
    Visualizes a graph using Graphviz with enhanced styling.

    Args:
        graph: Node key -> list of neighbor keys
        highlight: key -> color
        directed: bool - If True, uses Digraph (Directed), else Graph (Undirected).
        engine: str - Layout engine. 'dot' is best for DAGs/Hierarchies.
    """

    if highlight is None:
        highlight = {}
    if highlight_edges is None:
        highlight_edges = {}

    # 1. Initialize the Graphviz object
    if directed:
        dot = graphviz.Digraph(comment="Graph Visualization")
    else:
        dot = graphviz.Graph(comment="Graph Visualization")

    # 2. Configure the Layout Engine
    dot.engine = engine

    # 3. Global Styling (Prettier Defaults)
    dot.attr(rankdir="TB")  # Top-to-Bottom layout
    dot.attr(bgcolor="#100F22")
    dot.attr(splines="ortho")

    dot.attr(
        "node",
        shape="box",
        style="filled",
        fillcolor="#101019",
        color="#333340",
        fontcolor="#CCCCCC",
        fontname="Helvetica",
        penwidth="1.5",
    )

    dot.attr(
        "edge",
        color="#CCCCCC",
        arrowsize="0.3",
        fontname="Helvetica",
        arrowhead=arrowheads,
    )

    # 4. Add Nodes (Handle Highlighting)
    all_nodes = set(graph)
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for node in all_nodes:
        dot.node(node, fillcolor=highlight.get(node))

    # 5. Add Edges
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            dot.edge(
                node,
                neighbor,
                color=highlight_edges.get((node, neighbor)),
            )

    try:
        output_path = dot.render(filename, format="svg", cleanup=True)
        print(f"Graph successfully generated: {output_path}")
    except Exception as e:
        print(f"Error: Could not render graph.\nDetails: {e}")
        print(
            "Note: Ensure Graphviz executables are installed and in your system PATH."
        )
        print("Hint: sudo apt update && apt install xdot")


def get_path_elements(
    graph: Graph, start: str, end: str
) -> tuple[set[str], set[tuple[str, str]]]:
    """
    Returns a tuple (nodes, edges) containing all nodes and edges
    that are part of any valid path from start to end.
    """

    @cache
    def can_reach_end(curr: str):
        if curr == end:
            return True
        neighbors = graph.get(curr)
        if not neighbors:
            return False
        return any(can_reach_end(n) for n in graph[curr])

    nodes = set()
    edges = set()

    if not can_reach_end(start):
        return nodes, edges

    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        if not can_reach_end(node):
            continue
        nodes.add(node)

        if node not in graph:
            continue
        for neighbor in graph[node]:
            if can_reach_end(neighbor):
                edges.add((node, neighbor))
                stack.append(neighbor)

    return nodes, edges


if __name__ == "__main__":
    from pathlib import Path
    from sys import argv

    fname = "11s" if "-s" in argv else "11"

    here = Path(__file__).parent
    lines = (
        (here.parent / "inputs" / fname).with_suffix(".txt").read_text().splitlines()
    )
    dag = {}
    for line in lines:
        parts = line.strip().split()
        dag[parts[0].rstrip(":")] = parts[1:]

    _, p1_edges = get_path_elements(dag, "you", "out")
    nodes = ["svr", "fft", "dac", "out"]
    p2_edges = set()
    for i, start in enumerate(nodes[:-1]):
        dest = nodes[i + 1]
        _, edges = get_path_elements(dag, start, dest)
        p2_edges |= edges

    generic_pretty_graph(
        dag,
        highlight={
            "you": "#009900",
            "out": "#009900",
            "svr": "#C50F1F",
            "fft": "#881798",
            "dac": "#881798",
        },
        highlight_edges={
            **{e: "#ffff66" for e in p2_edges},
            **{e: "#009900" for e in p1_edges},
        },
        filename=str(here / fname),
    )
