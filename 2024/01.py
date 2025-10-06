"""--- Day 1: Historian Hysteria ---"""

from collections import Counter

from common import do_part_on_input, lines


def parse_row(row: str):
    return map(int, row.rstrip().split("   "))


def read_cols(filename: str) -> tuple[list[int], list[int]]:
    c0, c1 = [], []
    for line in lines(filename):
        v0, v1 = parse_row(line)
        c0.append(v0)
        c1.append(v1)
    return sorted(c0), sorted(c1)


def part1(filename: str):
    c0, c1 = read_cols(filename)
    s = 0
    for i, v in enumerate(c0):
        v1 = c1[i]
        s += abs(v - v1)
    return s


def part2(filename: str):
    c0, c1 = read_cols(filename)
    co1 = Counter(c1)
    return sum(i * co1.get(i, 0) for i in c0)


def main():
    do_part_on_input(1, part1)
    do_part_on_input(2, part2)


if __name__ == "__main__":
    main()
