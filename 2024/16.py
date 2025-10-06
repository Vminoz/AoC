"""--- Day 16: Reindeer Maze ---"""

from heapq import heappop, heappush
from typing import TypeAlias

from common import do_part_on_input, lines, logger
from common.maths import P2D
from common.visuals import p2d_sets_string

Maze: TypeAlias = tuple[set[P2D], P2D, P2D]
State: TypeAlias = tuple[int, P2D, P2D]
DEER = "𐂂"
CLOCKWISE: dict[P2D, P2D] = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}
COUNTERCLOCKWISE = {v: k for k, v in CLOCKWISE.items()}
TURN_COST = 1000
MOVE_COST = 1


def read_maze(filename: str) -> Maze:
    walls: set[P2D] = set()
    start, end = (-1, -1), (-1, -1)
    for i, line in enumerate(lines(filename)):
        for j, c in enumerate(line):
            if c == "#":
                walls.add((i, j))
            elif c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)

    if logger.is_debug:
        logger.m(
            p2d_sets_string(
                symbols={start: "S", end: "E"},
                secondary_set=walls,
            )
        )
    return walls, start, end


def lowest_score_path(maze: Maze, keep_all: bool = False) -> tuple[int, int]:
    walls, start, end = maze
    d = (0, 1)
    state = (0, start, d)
    queue: list[State] = [state]  # cost, position, direction, path
    visited: set[P2D] = set()
    paths_to: dict[tuple[P2D, P2D], tuple[int, set[P2D]]] = {(start, d): (0, {start})}
    best_cost = 1_000_000_000_000
    best_paths = set()
    while queue:
        cost, pos, d = heappop(queue)
        st = pos, d

        if pos in visited and not keep_all:
            continue
        visited.add(pos)

        if cost > best_cost:
            break
        if pos == end:
            best_cost = cost
            best_paths.update(paths_to[st][1])

        # Step
        for nd in (d, CLOCKWISE[d], COUNTERCLOCKWISE[d]):
            npos = pos[0] + nd[0], pos[1] + nd[1]
            ncost = cost + MOVE_COST + TURN_COST * (d != nd)
            if npos not in walls:
                nst = (npos, nd)
                if nst in paths_to:
                    if paths_to[nst][0] < ncost:
                        continue
                    paths_to[nst] = (ncost, paths_to[nst][1] | paths_to[st][1])
                    if logger.is_debug:
                        logger.m(
                            p2d_sets_string(
                                symbols={
                                    **{p: " " for p in paths_to[st][1]},
                                    pos: DEER,
                                },
                                main_set=visited,
                                secondary_set=walls,
                            )
                        )
                else:
                    paths_to[nst] = ncost, paths_to[st][1] | {npos}
                    heappush(queue, (ncost, npos, nd))

    if logger.is_verbose:
        logger.m(
            p2d_sets_string(
                symbols={pos: DEER for pos in best_paths},
                secondary_set=walls,
            )
        )
    return best_cost, len(best_paths)


def get_lowest_cost(filename: str) -> int:
    maze = read_maze(filename)
    return lowest_score_path(maze)[0]


def count_best_path_positions(filename: str) -> int:
    maze = read_maze(filename)
    return lowest_score_path(maze, keep_all=True)[1]


def main():
    do_part_on_input(1, get_lowest_cost)
    do_part_on_input(2, count_best_path_positions)


if __name__ == "__main__":
    main()
