from collections import deque as DQ

from common import P2D, do_part_on_input, lines, logger
from common.visuals import p2d_sets_string

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def neighbors(i: int, j: int):
    return ((i + di, j + dj) for di, dj in DIRECTIONS)


def read_garden(filename: str):
    rocks = set()
    si, sj = 0, 0
    for i, line in enumerate(lines(filename)):
        for j, ch in enumerate(line):
            if ch == "#":
                rocks.add((i, j))
            elif ch == "S":
                si, sj = i, j
    return rocks, (si, sj), j + 1


def num_spots(rocks: set[P2D], start_pos: P2D, max_steps: int, mod: int = 0):
    visited = set()
    end_positions = set()
    queue = DQ([(start_pos, 0)])
    end_modulo = max_steps % 2
    while queue:
        pos, dist = queue.popleft()
        if pos in visited:
            continue
        if dist % 2 == end_modulo:
            end_positions.add(pos)
        visited.add(pos)
        if dist + 1 > max_steps:
            continue
        for ni, nj in neighbors(*pos):
            if mod:
                valid = (ni % mod, nj % mod) not in rocks
            else:
                valid = (ni, nj) not in rocks
            if valid:
                queue.append(((ni, nj), dist + 1))
    if logger.level > 1:
        logger.v(end_positions)
        logger.m(p2d_sets_string(end_positions, visited))
    return len(end_positions)


def part1(filename: str):
    rocks, start_pos, _ = read_garden(filename)
    return num_spots(rocks, start_pos, 64)


def extrapolate_quad(y0: float, y1: float, y2: float):
    """Returns a function matching the quadratic with
    f(0) = y0; f(1) = y1; f(2) = y2 ⇒
    [4 2 1 | y2]
    [1 1 1 | y1]
    [0 0 1 | y0]
    """
    a = (y2 - 2 * y1 + y0) / 2
    b = y1 - y0 - a
    c = y0

    def f(x: float) -> float:
        return a * x**2 + b * x + c

    return f


def part2(filename: str, target: int = 26501365):
    rocks, start_pos, edge_len = read_garden(filename)
    radius = edge_len // 2
    max_steps = [radius + edge_len * i for i in range(3)]
    y = [num_spots(rocks, start_pos, s, edge_len) for s in max_steps]
    x = (target - radius) // edge_len
    logger.v(max_steps, y, x)
    return int(extrapolate_quad(*y)(x))


def main():
    do_part_on_input(1, part1)
    do_part_on_input(2, part2)


if __name__ == "__main__":
    main()
