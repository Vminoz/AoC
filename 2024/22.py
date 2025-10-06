"""--- Day 22: Monkey Market ---"""

from collections import Counter, deque
from typing import TypeAlias, cast

from common import do_part_on_input, lines, logger

Seq: TypeAlias = tuple[int, int, int, int]
Profits: TypeAlias = Counter[Seq]

MAGIC_NUM = 1 << 24  # 16777216


def update_secret_num(sn: int) -> int:
    """
    mix := xor
    prune := % MAGIC_NUM
    1. Calculate the result of multiplying the secret number by 64.
    Then, mix this result into the secret number.
    Finally, prune the secret number.

    2. Calculate the result of dividing the secret number by 32.
    Round the result down to the nearest integer.
    Then, mix this result into the secret number.
    Finally, prune the secret number.

    3. Calculate the result of multiplying the secret number by 2048.
    Then, mix this result into the secret number.
    Finally, prune the secret number.
    """
    # 1
    sn = (sn ^ (sn * 64)) % MAGIC_NUM
    # 2
    sn = (sn ^ (sn // 32)) % MAGIC_NUM
    # 3
    sn = (sn ^ (sn * 2048)) % MAGIC_NUM
    return sn


def sum_nth_secret_num(filename: str, n: int = 2000) -> int:
    s = 0
    for line in lines(filename):
        sn = int(line)
        nsn = sn
        for _ in range(n):
            nsn = update_secret_num(nsn)
        logger.d(sn, nsn)
        s += nsn
    return s


def price_sequence_profits(sn: int, n: int, profits: Profits):
    seen = set()
    pr_hist: deque[int] = deque(maxlen=4)
    price = sn % 10
    for i in range(n):
        sn = update_secret_num(sn)
        new_price = sn % 10
        pr_hist.append(new_price - price)
        price = new_price
        if i < 3:
            continue
        seq = cast(Seq, tuple(pr_hist))
        if seq not in seen:
            profits[seq] += price
        seen.add(seq)


def get_best_seq(filename: str, n: int = 2000) -> int:
    profits: Profits = Counter()
    for line in lines(filename):
        price_sequence_profits(int(line), n, profits)
    return max(profits.values())


def main():
    do_part_on_input(1, sum_nth_secret_num)
    do_part_on_input(2, get_best_seq)


if __name__ == "__main__":
    main()
