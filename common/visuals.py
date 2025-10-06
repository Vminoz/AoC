import webbrowser
from pathlib import Path
from sys import argv

from .ansi import highlight
from .maths import P2D, BBox, tuple_ranges

W = 2 if "w" in "".join(argv) else 1


def p2d_sets_string(
    main_set: set[P2D] | None = None,
    secondary_set: set[P2D] | None = None,
    symbols: dict[P2D, str] | None = None,
    secondary_symbols: dict[P2D, str] | None = None,
    bounding_box: BBox | None = None,
) -> str:
    # Defaults
    main_set = main_set or set()
    secondary_set = secondary_set or set()
    symbols = symbols or {}
    secondary_symbols = secondary_symbols or {}
    if not any((main_set, secondary_set, symbols, secondary_symbols)):
        raise ValueError("Nothing to display")

    # Infer or get bounding box
    if bounding_box is None:
        ri, rj = tuple_ranges(
            main_set
            | secondary_set
            | set(symbols.keys())
            | set(secondary_symbols.keys())
        )
    else:
        if bounding_box.ndims != 2:
            raise ValueError("Bounding box must be 2D, got %dD" % bounding_box.ndims)
        ri, rj = bounding_box.to_ranges()

    # Build string representation
    block = ["┌" + "─" * len(rj) * W + "┐"]
    for i in ri:
        line = "│"
        for j in rj:
            hl = False
            p = (i, j)
            if p in symbols:
                c = symbols[p]
                hl = True
            elif p in secondary_symbols:
                c = secondary_symbols[p]
                hl = p in main_set
            elif p in main_set:
                c = "█"
                hl = True
            elif p in secondary_set:
                c = "█"
                hl = False
            else:
                c = "·" if W == 1 else " "

            c *= W
            if hl:
                c = highlight(c)
            line += c
        block.append(line + "│")
    block.append("└" + "─" * len(rj) * W + "┘")

    return "\n".join(block)


def make_polygon_svg(verts: list[P2D], sz: int = 800, file: Path | None = None):
    ri, rj = tuple_ranges(verts)
    _min = min(ri.start, rj.start) - 1e6
    _max = max(ri.stop, rj.stop) - _min + 1e6
    v_string = " ".join(
        f"{sz * (j - _min) / _max},{(sz * (i - _min) / _max)}" for i, j in verts
    )
    svg = " ".join(
        (
            '<svg xmlns="http://www.w3.org/2000/svg"',
            f'width="{sz}" height="{sz}"',
            'style="background-color:#0C0C0C">',
            f'<polygon points="{v_string}"',
            'fill="#C50F1F" stroke="#F9F1A5" stroke-width="0.5"/>',
            "</svg>",
        )
    )
    svg_file = file or Path("polygon.svg")
    with open(svg_file, "w") as f:
        f.write(svg)
    webbrowser.open(str(svg_file.absolute()), new=1)
