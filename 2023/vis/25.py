# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib",
#     "networkx",
# ]
# ///
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
