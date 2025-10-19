from functools import lru_cache

from common import do_part_on_input, lines, logger


def spring_conditions(filename: str, unfold: int = 1) -> int:
    res = 0
    for line in lines(filename):
        symbols, groups = line.split()
        groups = tuple(int(c) for c in groups.split(","))
        if unfold > 1:
            symbols = "?".join([symbols] * unfold)
            groups *= unfold
        cnt = arrangements(symbols, groups, False)
        res += cnt
        logger.v(symbols, groups, cnt)
    return res


def decr_left(t: tuple[int]):
    return (t[0] - 1,) + t[1:]


@lru_cache(maxsize=None)
def arrangements(symbols: str, groups: tuple[int], in_block: bool) -> int:
    if not groups:
        return "#" not in symbols
    if not symbols:
        return groups == (0,)

    next_sym = symbols[0]
    if in_block:
        if groups[0] == 0:  # End of group
            if next_sym == "#":
                return 0  # Too many #
            return arrangements(symbols[1:], groups[1:], False)
        if next_sym == ".":
            return 0  # Not enough #
        return arrangements(symbols[1:], decr_left(groups), True)

    cnt = 0
    if next_sym != ".":  # Enter group
        cnt += arrangements(symbols[1:], decr_left(groups), True)
    if next_sym != "#":  # Move along
        cnt += arrangements(symbols[1:], groups, False)
    logger.v(symbols, groups, cnt)
    return cnt


def main():
    do_part_on_input(1, spring_conditions)
    do_part_on_input(2, spring_conditions, unfold=5)


if __name__ == "__main__":
    main()
