"""--- Day 25: Code Chronicle ---"""

from typing import TypeAlias

from common import P2D, do_part_on_input, lines, logger
from common.visuals import p2d_sets_string

Key: TypeAlias = set[P2D]
Lock: TypeAlias = set[P2D]


def read_locks_keys(filename: str) -> tuple[list[Lock], list[Key]]:
    locks, keys = [], []
    parts: set[P2D] = set()
    i = 0
    for line in lines(filename):
        line = line.rstrip()
        if not line:
            i = 0
            continue
        if i == 0:
            parts = set()
            if line[0] == "#":
                locks.append(parts)
            else:
                keys.append(parts)

        parts.update((i, j) for j, c in enumerate(line) if c == "#")
        i += 1
    return locks, keys


def check_fit(key: Key, lock: Lock) -> bool:
    return not key & lock


def just_check_all_keys(filename: str) -> int:
    locks, keys = read_locks_keys(filename)
    if logger.is_debug:
        for lo in locks:
            logger.m(p2d_sets_string(lo))
        for ke in keys:
            logger.m(p2d_sets_string(ke))

    c = 0
    for lock in locks:
        for key in keys:
            fit = check_fit(key, lock)
            c += fit
            if logger.is_verbose:
                logger.m(
                    p2d_sets_string(
                        key | lock if fit else key & lock,
                        symbols={p: "█" for p in key & lock},
                        secondary_symbols={
                            **{p: "┃" for p in key},
                            **{p: "║" for p in lock},
                        },
                    )
                )
            logger.d(lock, key, fit)
    return c


def main():
    do_part_on_input(1, just_check_all_keys)


if __name__ == "__main__":
    main()
