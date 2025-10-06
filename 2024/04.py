"""--- Day 4: Ceres Search ---"""

from typing import TypeAlias

from common import do_part, lines, logger, parse_input_with
from common.maths import DIRECTIONS, P2D

Grid: TypeAlias = list[list[str]]
DD = {
    "UR": (-1, 1),
    "UL": (-1, -1),
    "DR": (1, 1),
    "DL": (1, -1),
}


def parse_grid(filename: str) -> Grid:
    g = []
    for line in lines(filename):
        g.append(list(line.rstrip()))
    return g


def count_xmasses(letter_grid: Grid) -> int:
    count = 0
    for i, row in enumerate(letter_grid):
        for j, c in enumerate(row):
            if c == "X":
                xmasses = sum(
                    check_letters((i, j), "MAS", letter_grid, d) for d in DIRECTIONS
                )
                count += xmasses
                logger.v(i, j, xmasses, count)

    return count


def check_letters(pos: P2D, letters: str, grid: Grid, direction: P2D) -> bool:
    i, j = pos
    di, dj = direction
    # gri, grj = range(), range()
    nl = len(letters)
    if not (0 <= i + nl * di < len(grid)) or not (0 <= j + nl * dj < len(grid[0])):
        return False

    for c in letters:
        ni, nj = i + di, j + dj
        if grid[ni][nj] != c:
            return False
        i, j = ni, nj
    return True


def count_mas_xs(letter_grid: Grid) -> int:
    count = 0
    for i, row in enumerate(letter_grid[1:-1], start=1):
        for j, c in enumerate(row[1:-1], start=1):
            if c == "A":
                # check ⟍
                if not (
                    sorted(letter_grid[i - 1][j - 1] + letter_grid[i + 1][j + 1])
                    == ["M", "S"]
                ):
                    continue
                # check ⟍
                if not (
                    sorted(letter_grid[i - 1][j + 1] + letter_grid[i + 1][j - 1])
                    == ["M", "S"]
                ):
                    continue
                count += 1

    return count


def main():
    letter_grid = parse_input_with(parse_grid)
    do_part(1, count_xmasses, letter_grid)
    do_part(2, count_mas_xs, letter_grid)


if __name__ == "__main__":
    main()
