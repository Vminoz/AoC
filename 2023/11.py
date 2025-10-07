from common import lines, logger, do_part_on_input
from common.input_parsing import argv_input_file


def stars_dist_bit(filename: str, expansion: int = 2):
    stars = []
    e_r = 0
    e_c = 0
    for i, r in enumerate(lines(filename)):
        for j, c in enumerate(r):
            if c == "#":
                stars.append((i, j))
                e_r |= 1 << i
                e_c |= 1 << j
    e_c ^= (1 << (j + 1)) - 1
    e_r ^= (1 << (i + 1)) - 1
    res = 0
    ns = len(stars)
    for i in range(ns - 1):
        s1_r, s1_c = stars[i]
        for j in range(i + 1, ns):
            s2_r, s2_c = stars[j]
            res += abs(s1_r - s2_r) + abs(s1_c - s2_c)
            res += (
                ((((1 << s1_r) - 1) ^ ((1 << s2_r) - 1)) & e_r).bit_count()
                + ((((1 << s2_c) - 1) ^ ((1 << s1_c) - 1)) & e_c).bit_count()
            ) * (expansion - 1)
    return res


def stars_dist(filename: str, expansion: int = 2):
    stars = []
    pop_r = set()
    pop_c = set()
    for i, r in enumerate(lines(filename)):
        for j, c in enumerate(r):
            if c == "#":
                stars.append((i, j))
                pop_c.add(j)
                pop_r.add(i)
    dist = {}
    ns = len(stars)
    for i in range(ns - 1):
        s1 = stars[i]
        for j in range(i + 1, ns):
            s2 = stars[j]
            dist[(i, j)] = sum(
                1 if r in pop_r else expansion for r in range(s1[0], s2[0])
            ) + sum(
                1 if c in pop_c else expansion for c in range(*sorted((s1[1], s2[1])))
            )
    return sum(dist.values())


def main():
    from sys import argv

    if "-b" in argv:
        logger.m("【stars_dist】 uses sets, 【stars_dist_bit】 uses bit masks")
        for f in (stars_dist, stars_dist_bit):
            logger.bench(f, argv_input_file(), _n_runs=50)
    do_part_on_input(1, stars_dist_bit)
    do_part_on_input(2, stars_dist_bit, expansion=1000000)


if __name__ == "__main__":
    main()
