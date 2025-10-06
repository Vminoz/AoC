"""--- Day 20: Race Condition ---"""

from common import P2D, do_part_on_input, lines, logger
from common.maths import neighbors_4
from common.visuals import p2d_sets_string


def read_track(filename: str) -> tuple[set[P2D], P2D, P2D]:
    walls = set()
    start = (-1, -1)
    end = (-1, -1)
    for i, line in enumerate(lines(filename)):
        for j, c in enumerate(line):
            if c == "#":
                walls.add((i, j))
            elif c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
    return walls, start, end


def get_main_path(walls: set[P2D], start: P2D, pos: P2D) -> dict[P2D, int]:
    """Returns map of position to distance from end"""
    dist = 0
    path = {pos: dist}
    while pos != start:
        dist += 1

        nbs = [nb for nb in neighbors_4(pos) if nb not in walls and nb not in path]
        if len(nbs) != 1:
            raise ValueError(f"forked {dist=}")
        pos = nbs[0]

        path[pos] = dist
    return path


def show_path(path: dict[P2D, int | str], bg: set[P2D], label: str = ""):
    logger.m(
        p2d_sets_string(
            symbols={
                p: str(v % 10) if isinstance(v, int) else v for p, v in path.items()
            },
            secondary_set=bg,
        )
        + label
    )


def get_shortcuts(path: dict[P2D, int], n: int) -> dict[tuple[P2D, P2D], int]:
    shorcuts: dict[tuple[P2D, P2D], int] = {}
    for p, dist in path.items():
        new_shorcuts = {}  # Positions on path reachable in n steps from p with shorter path
        for i in range(-n, n + 1):
            r = n - abs(i)
            for j in range(-r, r + 1):
                np = (p[0] + i, p[1] + j)
                steps = abs(i) + abs(j)
                saved = path.get(np, 0) - dist - steps
                if saved > 0:
                    new_shorcuts[(p, np)] = saved
        if logger.is_debug:
            show_path(
                {k[1]: v for k, v in new_shorcuts.items()} | {p: "X"}, set(path.keys())
            )

        shorcuts.update(new_shorcuts)

    return shorcuts


def count_long_shortcuts(filename: str, cutoff: int = 100, n: int = 2) -> int:
    walls, start, end = read_track(filename)
    path = get_main_path(walls, start, end)
    shorcuts = get_shortcuts(path, n)
    shorcuts = {p: v for p, v in shorcuts.items() if v >= cutoff}
    if logger.is_verbose:
        show_path({k[1]: v for k, v in shorcuts.items()}, walls)
    return len(shorcuts)


def main():
    do_part_on_input(1, count_long_shortcuts)
    do_part_on_input(2, count_long_shortcuts, n=20)


if __name__ == "__main__":
    main()
