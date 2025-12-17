"""--- Day 9: Movie Theater ---"""

from collections.abc import Generator, Iterable
from pathlib import Path
from typing import TypeAlias

from common import do_part_on_input, logger
from common.maths import P2D
from common.visuals import make_polygon_svg, p2d_sets_string

Edge: TypeAlias = tuple[P2D, P2D]

CLOCKWISE: dict[P2D, P2D] = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}
COUNTERCLOCKWISE = {v: k for k, v in CLOCKWISE.items()}


class RectPolygon:
    """Ordered polygon with orthogonal edges"""

    def __init__(self, verts: Iterable[P2D]) -> None:
        self.verts = list(verts)
        if len(self.verts) % 2:
            raise ValueError("Cannot make a RectPolygon with uneven number of verts")
        # Ensure polygon is counterclockwise
        if not is_counterclockwise(self.verts):
            self.verts.reverse()

    def edges(self) -> Generator[Edge]:
        num_verts = len(self.verts)
        for i, v in enumerate(self.verts):
            pv = self.verts[i - 1]
            yield pv, v
            if num_verts == 2:
                break

    def __contains__(self, other: "RectPolygon") -> bool:
        if len(other.verts) < 5:
            # If other is a rectangle (4 or 2 vertices), use optimized check
            return self._contains_rect(other)

        for o_edge in other.edges():
            oe = EdgeInfo(o_edge)
            for self_edge in self.edges():
                se = EdgeInfo(self_edge)
                if logger.is_debug:
                    self._log_edge_check(other.edges(), o_edge, self_edge)
                if (
                    oe.cd != se.cd  # perpendicular
                    and (  # self edge's fixed dim is in other's range
                        se.fixed_val in oe.inner_range
                    )
                    and (
                        (  # other edge's fixed dim is in self edge's range => inner ranges cross
                            oe.fixed_val in se.inner_range
                        )
                        or (  # self edge turns into other from other's edge
                            self_edge[0][se.cd] == oe.fixed_val
                            and CLOCKWISE[se.dir] == oe.dir
                        )
                        or (  # self edge turns into other from within other's edge
                            self_edge[1][se.cd] == oe.fixed_val
                            and COUNTERCLOCKWISE[se.dir] == oe.dir
                        )
                    )
                ):
                    return False
        return True

    def _contains_rect(self, rect: "RectPolygon") -> bool:
        """Optimized contains check when 'other' is known to be a rectangle"""
        i_all = [v[0] for v in rect.verts]
        j_all = [v[1] for v in rect.verts]
        rect_range = [[min(i_all), max(i_all)], [min(j_all), max(j_all)]]

        rect_center = (
            rect_range[0][0] + (rect_range[0][1] - rect_range[0][0]) // 2,
            rect_range[1][0] + (rect_range[1][1] - rect_range[1][0]) // 2,
        )
        is_inside = False

        for p1, p2 in self.edges():
            fd = int(p1[1] == p2[1])
            fixed_val = p1[fd]
            fixed_range = rect_range[fd]
            cd = fd ^ 1
            change_range = rect_range[cd]
            change_val = sorted((p1[cd], p2[cd]))

            if (
                # Sort of raycast
                fd == 0  # horizontal
                and fixed_val < rect_center[0]  # above rect
                and change_val[0] <= rect_center[1] < change_val[1]  # aligned
            ):
                # if rect is inside, it should have an uneven number of edges above its center point
                is_inside = not is_inside

            if not fixed_range[0] < fixed_val < fixed_range[1]:
                continue  # edge is somewhere else - ok
            # edge is  perpendicular and: [│ │ ─] or [│ ┼] or [│─│]

            if max(change_val[0], change_range[0]) < min(
                change_val[1], change_range[1]
            ):
                #  [│ ┼] or [│─│]
                return False
        return is_inside

    def _log_edge_check(self, edges, o_edge, self_edge):
        if len(self.verts) > 100:
            return
        oe = EdgeInfo(o_edge)
        se = EdgeInfo(self_edge)
        logger.m(
            p2d_sets_string(
                set(points_on_edge(self_edge)),
                {p for e in edges for p in points_on_edge(e)},
                {p: "O" for p in points_on_edge(o_edge)},
                {p: "X" for p in self.verts},
            )
            + f"\n{o_edge} | {oe.cd=} | {oe.inner_range} | {oe.dir}"
            + f"\n{self_edge} | {se.cd=} | {se.inner_range} | {se.dir}"
        )

    @classmethod
    def from_rect_corners(cls, a: P2D, b: P2D) -> "RectPolygon":
        if a[0] == b[0] or a[1] == b[1]:
            return cls((a, b))
        return cls((a, (a[0], b[1]), b, (b[0], a[1])))


class EdgeInfo:
    def __init__(self, edge: Edge) -> None:
        self.dir = edge_direction(edge)
        self.cd = int(self.dir[1] != 0)
        self.ordered = sorted(edge)
        self.inner_range = range(self.ordered[0][self.cd] + 1, self.ordered[1][self.cd])
        self.fixed_val = edge[0][self.cd ^ 1]


def is_counterclockwise(verts: list[P2D]) -> bool:
    """https://en.wikipedia.org/wiki/Shoelace_formula"""
    return (
        sum(
            (v[0] - verts[i - 1][0]) * (v[1] + verts[i - 1][1])
            for i, v in enumerate(verts)
        )
        < 0
    )


def points_on_edge(edge: Edge) -> Generator[P2D]:
    start, end = sorted(edge)
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            yield i, j


def edge_direction(edge):
    di = edge[1][0] - edge[0][0]
    dj = edge[1][1] - edge[0][1]
    ed = (di // max(abs(di), 1), dj // max(abs(dj), 1))
    assert ed in CLOCKWISE, f"{ed} not a valid direction ({edge=})"
    return ed


def rect_area(a: P2D, b: P2D) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def calc_largest_inner_rectangle_area(tiles: list[P2D]) -> int:
    bounds = RectPolygon(tiles)
    is_bounds_large = len(bounds.verts) > 100
    largest_rect = None
    largest_area = -1
    for i, t1 in enumerate(tiles):
        for t2 in tiles[i + 1 :]:
            area = rect_area(t1, t2)
            if area <= largest_area:
                continue
            rect = RectPolygon.from_rect_corners(t1, t2)
            rect_is_in_polygon = rect in bounds

            if rect_is_in_polygon:
                largest_rect = rect
                largest_area = area

            if logger.is_verbose:
                if not is_bounds_large:
                    symbol = "O" if rect_is_in_polygon else "X"
                    logger.m(
                        p2d_sets_string(
                            set(rect.verts),
                            {p for e in bounds.edges() for p in points_on_edge(e)},
                            symbols={t1: symbol, t2: symbol},
                        )
                        + str(area)
                    )
                elif rect_is_in_polygon:
                    logger.v(area, t1, t2)

    if largest_rect is None:
        raise ValueError(f"Found no rectangles for {tiles=}")

    if is_bounds_large:
        rect = largest_rect
        make_polygon_svg(
            bounds.verts,
            rect.verts,
            rect.verts[:-1] if rect.verts[0] in [t1, t2] else rect.verts[1:],
            file=Path(__file__).parent / "vis" / "09.svg",
        )

    return largest_area


def parse_tiles(filename: str) -> list[P2D]:
    return [
        (int(ln.split(",", 1)[0]), int(ln.split(",", 1)[1]))
        for ln in Path(filename).read_text().split("\n")
    ]


def largest_rectangle(filename: str) -> int:
    tiles = parse_tiles(filename)
    return max(rect_area(t1, t2) for i, t1 in enumerate(tiles) for t2 in tiles[i + 1 :])


def largest_bounded_rectangle(filename: str) -> int:
    tiles = parse_tiles(filename)
    return calc_largest_inner_rectangle_area(tiles)


def main():
    do_part_on_input(1, largest_rectangle)
    do_part_on_input(2, largest_bounded_rectangle)


if __name__ == "__main__":
    main()
