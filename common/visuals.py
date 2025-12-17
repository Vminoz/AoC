from itertools import cycle
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


def make_polygon_svg(*verts: list[P2D], sz: int = 800, file: Path | None = None):
    colors = ["#C50F1F", "#13A10E99", "#F9F1A533"]
    stroke = "#F9F1A5"
    all_verts = (v for polygon in verts for v in polygon)
    ri, rj = tuple_ranges(all_verts)
    _min_i, _max_i = ri.start, ri.stop
    _min_j, _max_j = rj.start, rj.stop
    range_i = _max_i - _min_i
    range_j = _max_j - _min_j
    scale = 0.9 * sz / max(range_i, range_j)
    offset_i = (_max_i + _min_i) / 2
    offset_j = (_max_j + _min_j) / 2

    svg = "\n".join(
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" style="background-color:#0C0C0C">',
            *(
                "\n".join(
                    (
                        '<polygon points="',
                        *(
                            f"{sz / 2 + scale * (j - offset_j)},{sz / 2 - scale * (i - offset_i)}"
                            for i, j in polygon
                        ),
                        f'" fill="{color}" stroke="{stroke}" stroke-width="0.5"/>',
                    )
                )
                for polygon, color in zip(verts, cycle(colors))
            ),
            "</svg>",
        )
    )
    svg_file = file or Path("polygon.svg")
    with open(svg_file, "w") as f:
        f.write(svg)
