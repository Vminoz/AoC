from collections.abc import Iterable

from common import do_part_on_input, lines, logger

DIRECTIONS = [-1, -1j, 1, 1j]


def direction_dist(d: complex):
    def f(x: complex):
        return -d.real * x.real - d.imag * x.imag

    return f


def roll_cycles(filename: str, n: int = int(1e9)):
    static_rocks, round_rocks, lc, cc = parse_rocks(filename)
    mem = {}
    for cycle in range(n):
        for d in DIRECTIONS:
            round_rocks = sorted(round_rocks, key=direction_dist(d))
            round_rocks = roll(static_rocks, round_rocks, d, (lc, cc))
        load = calc_load(lc, round_rocks)
        logger.v(" ↑ Cycle", cycle + 1, load)
        key = tuple(round_rocks)
        if key in mem and ((n - cycle - 1) % (cycle - mem[key])) == 0:
            break  # same state as after n
        mem[key] = cycle
    return load


def show_rocks(static_rocks: set[complex], round_rocks: set[complex]):
    imax = int(max(static_rocks | round_rocks, key=lambda x: x.real).real)
    jmax = int(max(static_rocks | round_rocks, key=lambda x: x.imag).imag)
    logger.m("【┌" + "─" * (jmax + 1) + "┐】")
    for i in range(imax + 1):
        line = "【│】"
        for j in range(jmax + 1):
            if i + j * 1j in static_rocks:
                line += "■"
                continue
            if i + j * 1j in round_rocks:
                line += "【●】"
                continue
            line += "."
        logger.m(line + "【│】")
    logger.m("【└" + "─" * (jmax + 1) + "┘】")


def roll_north(filename: str):
    static_rocks, round_rocks, lc, _ = parse_rocks(filename)
    stopped_rocks = roll(static_rocks, round_rocks)
    return calc_load(lc, stopped_rocks)


def calc_load(lc: int, rocks: Iterable[complex]):
    return int(sum(lc - p.real for p in rocks))


def roll(
    static_rocks: set[complex],
    round_rocks: list[complex],
    to: complex = -1,
    limit: tuple[int, int] = (int(1e3), int(1e3)),
) -> set[complex]:
    stopped_rocks = set()
    round_rocks.reverse()
    while round_rocks:
        p = round_rocks.pop() + to
        while (
            0 <= p.real < limit[0]
            and 0 <= p.imag < limit[1]
            and p not in static_rocks
            and p not in stopped_rocks
        ):
            p += to
        p -= to
        stopped_rocks.add(p)
    if logger.level > 1:
        show_rocks(static_rocks, stopped_rocks)
    return stopped_rocks


def parse_rocks(filename):
    static_rocks = set()
    round_rocks = []
    for i, line in enumerate(lines(filename)):
        for j, ch in enumerate(line):
            if ch == ".":
                continue
            if ch == "#":
                static_rocks.add(i + j * 1j)
                continue
            if ch == "O":
                round_rocks.append(i + j * 1j)
    lc = i + 1
    cc = j + 1
    return static_rocks, round_rocks, lc, cc


def main():
    do_part_on_input(1, roll_north)
    do_part_on_input(2, roll_cycles)


if __name__ == "__main__":
    main()
