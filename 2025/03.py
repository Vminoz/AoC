"""--- Day 3: Lobby ---"""

from collections.abc import Iterable

from common import do_part_on_input, lines, logger


def get_total_joltage(filename: str, digits: int = 2) -> int:
    tot = 0
    for line in lines(filename):
        ln = line.strip()
        pos = -1
        for i in range(digits - 1, -1, -1):
            target = ln[pos + 1 : -i] if i > 0 else ln[pos + 1 :]
            highest, pos = get_max_int(target, pos + 1)
            tot += highest * 10**i
            logger.d(ln, i, tot, highest)
    return tot


def get_max_int(it: Iterable, start: int) -> tuple[int, int]:
    highest = 0
    for i, c in enumerate(it, start):
        joltage = int(c)
        if joltage > highest:
            imax = i
            highest = joltage
    if highest == 0:
        raise ValueError(f"Expected at least one >0 in `{it}`")
    return highest, imax


def main():
    do_part_on_input(1, get_total_joltage)
    do_part_on_input(2, get_total_joltage, digits=12)


if __name__ == "__main__":
    main()
