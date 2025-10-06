"""--- Day 19: Linen Layout ---"""

from functools import cache

from common import do_part_on_input, lines, logger


def read_towels_patterns(filename: str) -> tuple[frozenset[str], list[str]]:
    towels = []
    patterns = []
    for i, line in enumerate(lines(filename)):
        if i == 0:
            towels = line.rstrip().split(", ")
            continue
        if i == 1:
            continue
        patterns.append(line.rstrip())

    return frozenset(towels), patterns


@cache
def num_possible_ways(
    pattern: str, lengths: tuple[int, ...], towels: frozenset[str]
) -> int:
    if pattern == "":
        return 1
    ways = 0
    for w in lengths:
        if w > len(pattern):
            return ways
        if pattern[:w] in towels:
            ways += num_possible_ways(pattern[w:], lengths, towels)
    return ways


def count_possible_patterns(filename: str, sum_arrangements: bool = False) -> int:
    towels, patterns = read_towels_patterns(filename)
    towel_lengths = tuple(sorted({len(t) for t in towels}))
    logger.v(towels, patterns, towel_lengths, sep="\n")
    c = 0
    for p in patterns:
        ways = num_possible_ways(p, towel_lengths, towels)
        logger.d(ways, p)
        c += ways if sum_arrangements else bool(ways)
    return c


def main():
    do_part_on_input(1, count_possible_patterns)
    do_part_on_input(2, count_possible_patterns, sum_arrangements=True)


if __name__ == "__main__":
    main()
