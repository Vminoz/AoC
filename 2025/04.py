"""--- Day 4: Printing Department ---"""

from collections.abc import Iterable
from typing import TypeAlias

from common import do_part_on_input, lines
from common.maths import P2D, neighbors_8

Grid: TypeAlias = list[list[bool]]


def parse_rolls(filename: str) -> Grid:
    grid = []
    for line in lines(filename):
        row: list[bool] = []
        grid.append(row)
        for c in line.strip():
            row.append(c == "@")
    return grid


def get_forklift_accessible(grid: Grid) -> list[P2D]:
    n_rows = len(grid)
    n_cols = len(grid[0])
    accessible = []
    for i, row in enumerate(grid):
        for j, is_roll in enumerate(row):
            if not is_roll:
                continue
            adjacent_rolls = 0
            for ni, nj in neighbors_8((i, j)):
                if -1 < ni < n_rows and -1 < nj < n_cols:
                    adjacent_rolls += grid[ni][nj]
            if adjacent_rolls < 4:
                accessible.append((i, j))
    return accessible


def remove_from_grid(grid: Grid, indices: Iterable[P2D]):
    for i, j in indices:
        grid[i][j] = False


def count_forklift_accessible(filename: str) -> int:
    grid = parse_rolls(filename)
    return len(get_forklift_accessible(grid))


def count_forklift_removable(filename: str) -> int:
    grid = parse_rolls(filename)
    total_removed = 0
    done = False
    while not done:
        accessible = get_forklift_accessible(grid)
        remove_from_grid(grid, accessible)
        n_removed = len(accessible)
        done = n_removed == 0
        total_removed += n_removed
    return total_removed


def main():
    do_part_on_input(1, count_forklift_accessible)
    do_part_on_input(2, count_forklift_removable)


if __name__ == "__main__":
    main()
