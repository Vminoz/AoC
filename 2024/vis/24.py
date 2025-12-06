# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "graphviz",
# ]
# ///
"""Visual --- Day 24: Crossed Wires ---"""

from pathlib import Path

import graphviz  # type:ignore


def read_circuit(file: Path) -> list[tuple[str, str, str, str]]:
    """Read circuit from file, returns (input_values, gate_connections)"""
    gates = []
    at_gates = False

    for line in file.read_text().splitlines():
        line = line.rstrip()
        if not line:  # Empty line marks start of gates
            at_gates = True
            continue

        if at_gates:
            w1, op, w2, _, out = line.split(" ")
            gates.append((w1, op, w2, out))

    return gates


def create_graph(name: str, gates: list[tuple[str, str, str, str]]) -> graphviz.Digraph:
    """Create a graphviz visualization of the circuit"""
    dot = graphviz.Digraph(name)

    # Set global graph attributes
    dot.attr(rankdir="TB")
    dot.attr("node", fontname="Monospace")
    dot.attr("edge", penwidth="1.2")
    dot.attr(bgcolor="white")

    # Input and output bits
    styles = {
        "x": {"fillcolor": "#aaaaf0", "shape": "box", "style": "filled"},
        "y": {"fillcolor": "#aaf0aa", "shape": "box", "style": "filled"},
        "z": {"fillcolor": "#f0aaaa", "shape": "box", "style": "filled"},
    }
    xs: set[str] = set()
    for w1, _, w2, out in gates:
        if w1.startswith("x"):
            xs.add(w1)
        if w2.startswith("x"):
            xs.add(w2)
    xl = sorted(xs)

    # Clusters per bit position
    for nx in sorted(xl):
        ny = nx.replace("x", "y")
        nz = nx.replace("x", "z")
        with dot.subgraph(name=f"cluster_{nx}") as c:
            c.node(nx, nx, **styles["x"])
            c.node(ny, ny, **styles["y"])
            c.node(nz + "o", nz, **styles["z"])
            c.edge(nx, ny, style="invis")
    nz = f"z{int(xl[-1][1:]) + 1:02}"
    dot.node(nz + "o", nz, **styles["z"])

    # Add gates and connections
    fmt = {
        "AND": {"label": "&", "shape": "invhouse", "width": "0.4", "fixedsize": "true"},
        "OR": {"label": "|", "shape": "circle", "width": "0.4", "fixedsize": "true"},
        "XOR": {"label": "^", "shape": "triangle", "width": "0.4", "fixedsize": "true"},
    }
    for w1, op, w2, out in sorted(gates, key=lambda x: x[3], reverse=True):
        dot.node(out, **fmt[op])
        dot.edge(w1, out)
        dot.edge(w2, out)
        if out.startswith("z"):
            dot.edge(out, out + "o")

    return dot


def render_graph(g: graphviz.Digraph, to: Path):
    print(f"Overwriting {to}")
    g.render(to, format="svg", cleanup=True)


def main():
    # NOTE: run 24.py first for the fixed circuit
    wd = Path(__file__).parent
    # Read both circuits
    orig_gates = read_circuit(wd / ".." / "inputs" / "24.txt")
    fixed_gates = read_circuit(wd / "24.txt")
    # Create visualizations
    orig_graph = create_graph("original", orig_gates)
    fixed_graph = create_graph("fixed", fixed_gates)

    # Save to files
    render_graph(orig_graph, wd / "24-original")
    render_graph(fixed_graph, wd / "24-fixed")


if __name__ == "__main__":
    main()
