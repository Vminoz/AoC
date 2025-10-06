from common import logger, do_part_on_input


def find_mirrors(filename: str, smudges: int = 0):
    patterns = open(filename).read().split("\n\n")
    res = 0
    for pat in patterns:
        rows = [line.rstrip() for line in pat.splitlines()]
        if top := mirror(rows, smudges):
            res += 100 * top
            show_mirror(rows, top, False)
            continue
        cols = transpose(rows)
        if left := mirror(cols, smudges):
            res += left
            show_mirror(cols, left, True)
            continue
        raise ValueError("mirror not found in:\n" + "\n".join(rows))
    return res


def transpose(rows):
    return ["".join(c) for c in zip(*rows)]


def show_mirror(rows, top, transposed):
    if logger.level > 1:
        logger.v("\n", rows[0], sep="", end="")
        logger.m("⊤" if transposed else "")
        for i, r in enumerate(rows[1:]):
            if i == top:
                logger.m(("─") * len(r) + f" ↑ {top}")
            logger.v(r, sep="")


def mirror(rows: list[str], smudges: int = 0) -> int:
    r_c = len(rows)
    for i in range(r_c - 1):
        j = i + 1
        top = j
        if valid_mirror(i, j, rows, r_c, smudges):
            return top
    return 0


def valid_mirror(i, j, rows, n_rows, smudges):
    smudged = False
    while i > -1 and j < n_rows:
        if diff := str_diff(rows[j], rows[i], smudges):
            if smudged or diff > smudges:
                return False
            smudged = True
        i -= 1
        j += 1
    return smudged == smudges


def str_diff(s1: str, s2: str, limit: int = 1) -> int:
    # they must have same length but not gonna check 😎
    if s1 == s2:
        return 0
    if not limit:
        return 1
    d = 0
    for ch1, ch2 in zip(s1, s2):
        if ch1 != ch2:
            d += 1
            if d > limit:
                return limit + 1
    return d


def main():
    do_part_on_input(1, find_mirrors)
    do_part_on_input(2, find_mirrors, smudges=1)


if __name__ == "__main__":
    main()
