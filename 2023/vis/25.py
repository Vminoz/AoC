# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib==3.10",
#     "networkx==3.6",
#     "scipy==1.16",
#     "PyQt5==5.15",
# ]
# ///
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def show_edge_graph(edges: dict[tuple[str, str], int]) -> None:
    G = nx.Graph()
    G.add_edges_from(edges.keys())
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(
        G,
        pos,
        edge_color="black",
        width=1,
        linewidths=1,
        node_size=500,
        node_color="pink",
        alpha=0.9,
        labels={node: node for node in G.nodes()},
    )
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edges,
        font_color="red",
    )
    plt.axis("off")
    plt.show()


def read_edges(from_file: Path):
    text = from_file.read_text()
    edges = {}
    for ln in text.split("\n"):
        s = ln.split("-")
        edges[(s[0], s[1])] = s[2]
    return edges


def main():
    graph_file = Path(__file__).parent / "--25.txt"
    try:
        edges = read_edges(graph_file)
    except FileNotFoundError:
        print(f"Missing file {graph_file} (run 2023/05.py)")
        sys.exit(1)
    show_edge_graph(edges)


if __name__ == "__main__":
    main()
