"""--- Day 18: RAM Run ---"""

from collections import deque
from typing import Generator, cast

from common import do_part_on_input, lines, logger
from common.input_parsing import USE_SMALL_FILE
from common.maths import P2D, BBox, neighbors_4
from common.visuals import p2d_sets_string

if USE_SMALL_FILE:
    BBOX = BBox(lower=(0, 0), upper=(6, 6))
    BYTES_FALLEN = 12
else:
    BBOX = BBox(lower=(0, 0), upper=(70, 70))
    BYTES_FALLEN = 1024


def read_block_coords(filename: str) -> Generator[P2D, None, None]:
    """Generator filling shared coords set"""
    for line in lines(filename):
        x, y = line.split(",")
        yield (int(y), int(x))


def get_shortest_path(blocks: set[P2D], bb: BBox) -> set[P2D]:
    start = (0, 0)
    end = bb.upper
    queue: deque[tuple[P2D, set[P2D]]] = deque([(start, set())])
    visited = set()
    steps = 0
    while queue:
        steps += 1
        pos, path = queue.popleft()
        if pos == end:
            return path
        if pos in visited:
            continue
        visited.add(pos)
        queue.extend(
            (nb, path | {pos})
            for nb in neighbors_4(pos)
            if nb not in blocks and nb in bb
        )

        if logger.is_debug and steps % 100 == 0:
            logger.m(
                p2d_sets_string(
                    symbols={pos: "O", **{p: " " for p in path}},
                    main_set=visited,
                    secondary_set=blocks,
                    bounding_box=BBOX,
                )
                + str(steps)
            )
    return set()


def find_shortest_path_length(filename: str) -> int:
    block_gen = read_block_coords(filename)
    blocks = set()
    for _ in range(BYTES_FALLEN):
        blocks.add(next(block_gen))
    path = get_shortest_path(blocks, BBOX)
    if logger.is_verbose:
        logger.m(
            p2d_sets_string(
                symbols={cast(P2D, BBOX.upper): "X"},
                main_set=path,
                secondary_set=blocks,
                bounding_box=BBOX,
            )
        )
    return len(path)


def find_first_blocking_block(filename: str) -> str:
    block_gen = read_block_coords(filename)
    blocks = set()
    for _ in range(BYTES_FALLEN):
        blocks.add(next(block_gen))
    path = get_shortest_path(blocks, BBOX)
    # We already know it's possible here from p1

    new_block = (-1, -1)
    while path:
        new_block = next(block_gen)
        blocks.add(new_block)
        if new_block not in path:
            continue
        path = get_shortest_path(blocks, BBOX)

    if logger.is_verbose:
        logger.m(
            p2d_sets_string(
                main_set={new_block},
                secondary_set=blocks,
                bounding_box=BBOX,
            )
        )
    return ",".join(map(str, reversed(new_block)))


def main():
    do_part_on_input(1, find_shortest_path_length)
    do_part_on_input(2, find_first_blocking_block)


if __name__ == "__main__":
    main()
