"""--- Day 11: Plutonian Pebbles ---"""

from functools import cache

from common import do_part_on_input, logger


def read_stones(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(i) for i in f.read().strip().split()]


def count_stones_after_blinks(filename: str, blinks: int) -> int:
    stones = read_stones(filename)
    count = 0
    for s in stones:
        count += get_num_stones(s, blinks)
        logger.v(s, count)
    return count


@cache
def update(num: int) -> tuple[int, ...]:
    if num == 0:
        return (1,)
    s = str(num)
    d = len(s)
    if d % 2 == 0:
        return int(s[: d // 2]), int(s[d // 2 :])
    return (2024 * num,)


@cache
def get_num_stones(num: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    return sum(get_num_stones(n, blinks - 1) for n in update(num))


def main():
    do_part_on_input(1, count_stones_after_blinks, blinks=25)
    do_part_on_input(2, count_stones_after_blinks, blinks=75)


if __name__ == "__main__":
    main()
