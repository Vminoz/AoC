"""--- Day 2: I Was Told There Would Be No Math ---"""

from pathlib import Path

from common import do_part_on_input, logger


def sum_invalid_ids(filename: str, extras: bool = False) -> int:
    ranges = Path(filename).read_text().split(",")
    res = 0
    for r in ranges:
        st, ed = (int(e) for e in r.split("-", 1))
        for i in range(st, ed + 1):
            s = str(i)
            sl = len(s)
            mid = sl // 2
            if mid == 0 or (not extras and sl % 2):
                continue
            to_check = range(mid, 0, -1) if extras else (mid,)
            for j in to_check:
                if sl % j:
                    continue
                ref = s[:j]
                same = True
                for k in range(j, sl, j):
                    buf = s[k : k + j]
                    same = buf == ref
                    if not same:
                        break
                logger.d(r, s, j, same)
                if same:
                    res += i
                    logger.d(r, j, ref, res, s)
                    break

    return res


def main():
    do_part_on_input(1, sum_invalid_ids)
    do_part_on_input(2, sum_invalid_ids, extras=True)


if __name__ == "__main__":
    main()
