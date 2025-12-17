"""--- Day 12: Christmas Tree Farm ---"""

from collections.abc import Container, Iterable
from dataclasses import dataclass
from functools import cache, reduce
from operator import add
from pathlib import Path

from common import do_part_on_input, logger
from common.maths import P2D
from common.visuals import p2d_sets_string


@dataclass(frozen=True)
class Shape:
    """A shape represented by a normalized set of points."""

    points: frozenset[P2D]

    def __post_init__(self):
        if not self.points:
            raise ValueError("No points in shape")
        if (min(i for i, _ in self.points), min(j for _, j in self.points)) != (0, 0):
            raise ValueError("Shape should be aligned with (0,0)")

    @classmethod
    def from_points(cls, pts: Iterable[P2D]) -> "Shape":
        """Take points and ensure they are aligned with 0,0"""
        min_i = min(i for i, _ in pts)
        min_j = min(j for _, j in pts)
        normalized_pts = frozenset((i - min_i, j - min_j) for i, j in pts)
        return cls(normalized_pts)

    @property
    @cache
    def size(self) -> P2D:
        return (max(i for i, _ in self.points) + 1, max(j for _, j in self.points) + 1)

    def __str__(self) -> str:
        def sym(i, j):
            return "█" if (i, j) in self.points else "·"

        lines = (
            reduce(add, (sym(i, j) for j in range(self.size[1])), "")
            for i in range(self.size[0])
        )
        return "\n".join(lines)

    def flipped(self) -> "Shape":
        """Return a copy flipped horizontally"""
        return self.from_points([(i, -j) for i, j in self.points])

    def rotated(self) -> "Shape":
        """Return a copy rotated clockwise"""
        return self.from_points([(j, -i) for i, j in self.points])

    @cache
    def get_orientations(self) -> "set[Shape]":
        same = self.from_points(self.points)
        unique_forms: set[Shape] = {same}
        # Flipped
        flipped = self.flipped()
        unique_forms.add(self.flipped())

        # Rotations
        for _ in range(3):
            same = same.rotated()
            unique_forms.add(same)
            flipped = flipped.rotated()
            unique_forms.add(flipped)

        if logger.is_verbose:
            self._log_forms(unique_forms)

        return unique_forms

    @staticmethod
    def _log_forms(forms: "Iterable[Shape]"):
        s: list[str] = []
        for form in forms:
            form_lines = str(form).split()
            if not s:
                s = form_lines
                continue
            for j, ln in enumerate(form_lines):
                for _ in range(j - len(s) + 1):
                    s.append(" " * len(s[0]))
                s[j] += " " + ln
        logger.m("\n".join(s) + "\n")


@dataclass
class Region:
    size: P2D
    num_shapes: tuple[int, ...]  # how many of each shape

    def __post_init__(self) -> None:
        i_max, j_max = self.size
        self.area = i_max * j_max
        self.i_range = range(i_max)
        self.j_range = range(j_max)

        self.occupied: set[P2D] = set()
        self.shape_at: dict[P2D, int] = {}
        self.shapes: list[Shape] = []
        self.shape_orientations: list[set[Shape]] = []
        self.to_place: list[int] = []
        self._wont_fit: bool = False

    @classmethod
    def from_string(cls, s: str) -> "Region":
        parts = s.split()
        sz = [int(n) for n in parts[0].rstrip(":").split("x")]
        num_presents = [int(p) for p in parts[1:]]
        return cls((sz[0], sz[1]), tuple(num_presents))

    def __str__(self) -> str:
        return f"{self.size[0]}x{self.size[1]}: " + " ".join(
            str(n) for n in self.num_shapes
        )

    def __contains__(self, p: P2D) -> bool:
        return (p[0] in self.i_range) and (p[1] in self.j_range)

    def load_shapes(self, shapes: list[Shape]):
        self.shapes = shapes
        self.shape_orientations = [s.get_orientations() for s in shapes]

        self.to_place = []
        for i, count in enumerate(self.num_shapes):
            self.to_place.extend([i] * count)

        # Reset state
        self.occupied.clear()
        self.shape_at.clear()
        minimum_area = sum(len(shapes[i].points) for i in self.to_place)
        self._wont_fit = self.area < minimum_area

    def fit(self) -> bool:
        if self._wont_fit:
            return False
        return self._fit_backtrack(0)

    def _fit_backtrack(self, idx_to_place: int) -> bool:
        """Naive check if shapes fit
        - luckily all input lines where region.area < shapes.area turn out to have a lot of margin
        """
        # Base Case: All shapes placed
        if idx_to_place == len(self.to_place):
            return True

        shape_idx = self.to_place[idx_to_place]
        orientations = self.shape_orientations[shape_idx]

        for i in self.i_range:
            for j in self.j_range:
                for shape in orientations:
                    # Check if shape fits if anchored at (i, j)
                    points_to_occupy = set()
                    can_place = True
                    for di, dj in shape.points:
                        p = (i + di, j + dj)
                        if p not in self or p in self.occupied:
                            can_place = False
                            break
                        points_to_occupy.add(p)

                    if can_place:
                        # Place and recurse
                        self.occupied |= points_to_occupy
                        if logger.is_debug:
                            logger.m(self.pretty_str(points_to_occupy))

                        # Recurse for the next shape in the list
                        if self._fit_backtrack(idx_to_place + 1):
                            self.shape_at |= {p: shape_idx for p in points_to_occupy}
                            return True

                        # Backtrack (undo placement)
                        self.occupied -= points_to_occupy
        return False

    def pretty_str(self, highlights: Container[P2D] = ()) -> str:
        def SGR(x):
            return f"\033[{x}m"

        bright_colors = [SGR(n) for n in range(91, 97)]
        rst = SGR("")

        lines = ["┌" + "─" * len(self.j_range) + "┐"]
        for i in self.i_range:
            line = "│"
            for j in self.j_range:
                c = "·"
                if self.shape_at:
                    shape_idx = self.shape_at.get((i, j))
                    if shape_idx:
                        color = bright_colors[shape_idx % len(bright_colors)]
                        c = f"{color}{shape_idx}{rst}"
                else:
                    if (i, j) in self.occupied:
                        color_idx = 2 if (i, j) in highlights else 0
                        c = f"{bright_colors[color_idx]}█{rst}"
                line += c
            lines.append(line + "│")
        lines.append("└" + "─" * len(self.j_range) + "┘")
        return rst + "\n".join(lines)


def parse_presents(filename: str) -> tuple[list[Shape], list[Region]]:
    lines = Path(filename).read_text().split("\n")
    shapes = []
    regions = []
    shape_row = -1
    points: set[P2D] = set()
    for ln in lines:
        if not ln:
            if points:  # Collect shape
                logger.d(points)
                sh = Shape.from_points(points)
                shapes.append(sh)
                points = set()
                shape_row = -1
            continue
        if ln[-1] == ":":  # Start of shape
            shape_row = 0
            continue
        if shape_row > -1:
            points.update((shape_row, j) for j, c in enumerate(ln) if c == "#")
            shape_row += 1
            continue

        # Region line
        regions.append(Region.from_string(ln))
    return shapes, regions


def count_fitting_regions(filename: str) -> int:
    shapes, regions = parse_presents(filename)

    res = 0
    for i, region in enumerate(regions):
        region.load_shapes(shapes)
        success = region.fit()
        res += int(success)

        logger.v(f"{i + 1}: {region} →", "FITS" if success else "FAIL")
        if success and logger.is_verbose:
            logger.m(
                p2d_sets_string(symbols={p: str(s) for p, s in region.shape_at.items()})
            )

    return res


def main():
    do_part_on_input(1, count_fitting_regions)


if __name__ == "__main__":
    main()
