from collections import defaultdict

from common import do_part_on_input, logger


def apply_wierd_hash(filename: str):
    res = 0
    for s in open(filename).read().split(","):
        res += wierd_hash(s)
    return res


def wierd_hash(s: str):
    cv = 0
    for c in s:
        cv += ord(c)
        cv *= 17
        cv %= 256
    return cv


def not_val(val):
    def f(x):
        return x[0] != val

    return f


def box_stuff(filename: str):
    hm = defaultdict(dict)
    for s in open(filename).read().split(","):
        if s.endswith("-"):
            s = s[:-1]
            h = wierd_hash(s)
            if h in hm:
                hm[h].pop(s, 0)
        else:
            s, n = s.split("=")
            h = wierd_hash(s)
            hm[h][s] = int(n)
    logger.v(hm)
    return sum(
        (1 + k) * sum((i + 1) * fl for i, fl in enumerate(v.values()))
        for k, v in hm.items()
    )


def main():
    do_part_on_input(1, apply_wierd_hash)
    do_part_on_input(2, box_stuff)


if __name__ == "__main__":
    main()
