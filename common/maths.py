from dataclasses import dataclass
from math import gcd
from typing import Iterable, Iterator, TypeAlias

P2D: TypeAlias = tuple[int, int]
P3D: TypeAlias = tuple[int, int, int]

DIRECTIONS = (
    # +
    (-1, 0),  # U
    (1, 0),  # D
    (0, -1),  # L
    (0, 1),  # R
    # ×
    (-1, 1),  # UR
    (-1, -1),  # UL
    (1, 1),  # DR
    (1, -1),  # DL
)
D4 = DIRECTIONS[:4]


def neighbors_4(p: P2D):
    i, j = p
    return ((i + di, j + dj) for di, dj in DIRECTIONS[:4])


def neighbors_8(p: P2D):
    i, j = p
    return ((i + di, j + dj) for di, dj in DIRECTIONS)


@dataclass
class F2D:
    x: float
    y: float


@dataclass
class F3D:
    x: float
    y: float
    z: float

    def __add__(self, other: "F3D") -> "F3D":
        return F3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: "F3D") -> "F3D":
        return F3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, other: float) -> "F3D":
        return F3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float) -> "F3D":
        return F3D(self.x / other, self.y / other, self.z / other)

    def __matmul__(self, other: "F3D") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "F3D") -> "F3D":
        return F3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y, self.z))


@dataclass
class BBox:
    """N-dimensional closed interval"""

    lower: tuple[float, ...]
    upper: tuple[float, ...]

    @property
    def ndims(self) -> int:
        return len(self.lower)

    def __post_init__(self):
        lower_dims = len(self.lower)
        upper_dims = len(self.upper)
        if lower_dims != upper_dims:
            raise ValueError(
                "Lower and upper bounds must have the same dimensions, not %d and %d"
                % (lower_dims, upper_dims)
            )
        self.fspan = tuple(ub - lb for ub, lb in zip(self.upper, self.lower))
        self.ispan = tuple(int(r + 1) for r in self.fspan)

    def __contains__(self, p: tuple[float, ...] | F2D | F3D):
        if isinstance(p, F2D):
            p = (p.x, p.y)
        elif isinstance(p, F3D):
            p = (p.x, p.y, p.z)
        elif len(p) != self.ndims:
            raise ValueError(f"Expected {self.ndims}D point, got {len(p)}D")

        return all(
            lower <= p <= upper for p, lower, upper in zip(p, self.lower, self.upper)
        )

    @classmethod
    def from_tuples(cls, pairs: Iterable[tuple[int, ...]]):
        ranges = tuple_ranges(pairs)
        return cls(tuple(r.start for r in ranges), tuple(r.stop - 1 for r in ranges))

    def to_ranges(self) -> list[range]:
        """Return the integer positions within the bounding box as a list of ranges for each dimension"""
        return [range(int(lb), int(ub) + 1) for lb, ub in zip(self.lower, self.upper)]


def tuple_ranges(pairs: Iterable[tuple[int, ...]]) -> tuple[range, ...]:
    """Turn an iterable of tuples into their n-D bounding box"""
    return tuple(range(min(x), max(x) + 1) for x in zip(*pairs))


def shoelace_area(verts: list[P2D]) -> int:
    """https://en.wikipedia.org/wiki/Shoelace_formula#Triangle_form,_determinant_form"""
    assert verts[-1] == verts[0]
    return (
        sum(
            v[0] * verts[i + 1][1] - v[1] * verts[i + 1][0]
            for i, v in enumerate(verts[:-1])
        )
        // 2
    )


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def bones(v: int) -> int:
    return bin(v).count("1")
