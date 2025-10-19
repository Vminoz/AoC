from math import ceil, sqrt

from common import do_part_on_input, lines, logger


def qraces(filename: str):
    T, D = (map(int, s.rstrip().split()[1:]) for s in lines(filename))
    prod = 1
    for t, d in zip(T, D):
        # Integers covered by the reange between roots of -x^2+tx-d=0
        prod *= neg_quad_root_int_range(t, d)
    return prod


def neg_quad_root_int_range(b, c):
    sq = sqrt(b**2 - 4 * c)
    lower = 0.5 * (b - sq)
    rg_adj = ceil(sq) - (lower - int(lower) < 0.5)
    logger.v(b, c, lower, sq, "\n\t→", rg_adj)
    return rg_adj


def qrace(filename: str):
    t, d = (int(s.rstrip().replace(" ", "").split(":")[1]) for s in lines(filename))
    return neg_quad_root_int_range(t, d)


def main():
    do_part_on_input(1, qraces)
    do_part_on_input(2, qrace)


if __name__ == "__main__":
    main()
