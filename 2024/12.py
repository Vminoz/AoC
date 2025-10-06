"""--- Day 12: Garden Groups ---"""

from collections import defaultdict, deque

from common import do_part, logger, parse_input_with
from common.maths import D4, P2D, bones, neighbors_4
from common.visuals import p2d_sets_string


def read_grid(filename: str) -> list[str]:
    # sometimes more convenient:
    with open(filename) as f:
        grid = f.read().split("\n")
    return grid


def fence_cost(grid: list[str], bulk: bool = False) -> int:
    visited = set()
    cost = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if (i, j) in visited or c == ".":
                continue
            area, perimeter = get_area_perimeter((i, j), grid)
            visited |= area
            if bulk:
                apply_discount(perimeter)
            price = fence_price(area, perimeter)
            cost += price

            if logger.is_verbose:
                logger.m(
                    p2d_sets_string(
                        symbols={p: c for p in area},
                        secondary_symbols={
                            p: str(bones(v)) for p, v in perimeter.items()
                        },
                    )
                    + f"{price}"
                )

    return cost


def fence_price(area: set[P2D], perimeter: dict[P2D, int]) -> int:
    return len(area) * sum(bones(v) for v in perimeter.values())


def apply_discount(perimeter: dict[P2D, int]) -> None:
    """
    For each point, discount neighbors in each direction
    as long as they share a fence direction (4-bit represented)
    """
    for p, v in perimeter.items():
        for d in D4:
            n = (p[0] + d[0], p[1] + d[1])
            shared = v
            while shared and n in perimeter:
                nv = perimeter[n]
                shared &= nv
                perimeter[n] -= shared
                n = (n[0] + d[0], n[1] + d[1])

        if logger.is_debug:
            logger.m(
                p2d_sets_string(
                    main_set={p},
                    secondary_symbols={p: str(bones(v)) for p, v in perimeter.items()},
                )
            )


def get_area_perimeter(p: P2D, grid: list[str]) -> tuple[set[P2D], dict[P2D, int]]:
    """returns the points on the perimeter of the region"""
    q = deque([p])
    v = grid[p[0]][p[1]]
    area = {p}
    perimeter: dict[P2D, int] = defaultdict(int)
    while q:
        p = q.popleft()
        for i, n in enumerate(neighbors_4(p)):
            if n in area:
                continue
            if (
                (0 <= n[0] < len(grid))
                and (0 <= n[1] < len(grid[0]))
                and (grid[n[0]][n[1]] == v)  # same region
            ):
                q.append(n)
                area.add(n)
            else:
                perimeter[n] += 1 << i
    return area, perimeter


def main():
    grid = parse_input_with(read_grid)
    do_part(1, fence_cost, grid)
    do_part(2, fence_cost, grid, bulk=True)


if __name__ == "__main__":
    main()
