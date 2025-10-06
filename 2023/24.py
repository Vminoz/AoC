from dataclasses import dataclass
import re
from common import lines, do_part_on_input, logger
from common.maths import F3D, BBox, F2D
from itertools import combinations

SMALL_BOX = BBox((7, 7), (27, 27))
BIG_BOX = BBox((2e14, 2e14), (4e14, 4e14))


@dataclass
class Stone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    def __post_init__(self):
        if any(d == 0 for d in (self.dx, self.dy, self.dz)):
            raise ValueError("Cannot have zero velocity")
        self.xy_slope = self.dy / self.dx
        self.p = F3D(self.x, self.y, self.z)
        self.v = F3D(self.dx, self.dy, self.dz)

    def line_intersection_2d(self, other: "Stone") -> F2D | None:
        if self.xy_slope == other.xy_slope:
            return None  # Parallel

        x_intersect = (
            other.y - self.y + self.xy_slope * self.x - other.xy_slope * other.x
        ) / (self.xy_slope - other.xy_slope)
        y_intersect = self.y + self.xy_slope * (x_intersect - self.x)

        return F2D(x_intersect, y_intersect)

    def future_intersection(self, other: "Stone"):
        intersection = self.line_intersection_2d(other)
        if intersection is None:
            return None

        # Calculate the time at which each stone reaches the intersection point
        self_time = (intersection.x - self.x) / self.dx
        other_time = (intersection.x - other.x) / other.dx

        if self_time < 0 or other_time < 0:
            return None  # Intersection point is in the past

        return intersection


def count_intersections_within_bounds(filename: str) -> int:
    stones = parse_stones(filename)
    BBOX = SMALL_BOX if len(stones) < 10 else BIG_BOX

    cnt = 0
    for a, b in combinations(stones, 2):
        logger.v("\n", a, b, sep="⟋")
        intersection = a.future_intersection(b)
        if not intersection:
            continue
        logger.v(intersection, intersection in BBOX)
        cnt += intersection in BBOX
    return cnt


def parse_stones(filename: str) -> list[Stone]:
    re_int = re.compile(r"-?\d+")
    stones = [Stone(*(int(s) for s in re_int.findall(s))) for s in lines(filename)]
    return stones


def find_line_intersecting_all(filename: str) -> int:
    stones = parse_stones(filename)

    s0, s1, s2 = stones[:3]
    # Use s0 as reference frame
    p1, p2 = s1.p - s0.p, s2.p - s0.p
    v1, v2 = s1.v - s0.v, s2.v - s0.v

    # c1 × c1 = 0 since they must be aligned from the perspective of s0
    # ⇔ (p1+v1t1) × (p2+v2t2) = 0
    # (E1) ⇔ p1×p2 + v1t1×p2 + p1×v2t2 + t1t2(v1×v2) = 0
    # * (E1•v2) ⇒ (p1×p2)•v2 + t1(v1×p2)•v2 = 0
    #           ⇔ t1= -(p1×p2)•v2/(v1×p2)•v2
    # * (E1•v1) ⇒ t2 = -(p1×p2)•v1/(p1×v2)•v1
    #
    p1xp2 = p1.cross(p2)
    t1 = -((p1xp2 @ v2) / (v1.cross(p2) @ v2))
    t2 = -((p1xp2 @ v1) / (p1.cross(v2) @ v1))

    # Note: back to absolute coordinates
    collision_1 = s1.p + s1.v * t1
    collision_2 = s2.p + s2.v * t2
    v = (collision_2 - collision_1) / (t2 - t1)
    p = collision_1 - v * t1
    logger.v(f"@{t1=}: {collision_1}\n@{t2=}: {collision_2}\n{v=}\n{p=}")
    return int(sum(p))


def main():
    do_part_on_input(1, count_intersections_within_bounds)
    do_part_on_input(2, find_line_intersecting_all)


if __name__ == "__main__":
    main()
