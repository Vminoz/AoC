"""--- Day 2: Gift Shop ---"""

from pathlib import Path

from common import do_part_on_input, logger


def sum_invalid_ids(filename: str, extras: bool = False) -> int:
    ranges = Path(filename).read_text().split(",")
    res = 0
    for r in ranges:
        st, ed = (int(e) for e in r.split("-", 1))
        ids_in_range = set()

        digits_range = range(len(str(st)), len(str(ed)) + 1)
        # Logarithms? Never hear of him
        for digits in digits_range:
            if digits == 0 or (not extras and digits % 2):
                continue

            mid = digits // 2
            to_check = (
                [split for split in range(1, mid + 1) if digits % split == 0]
                if extras
                else [mid]
            )

            for j in to_check:
                repeats = digits // j
                for pattern in range(10 ** (j - 1), 10**j):
                    id_ = str(pattern) * repeats
                    id_val = int(id_)
                    if st <= id_val <= ed:
                        logger.d(r, j, id_val)
                        ids_in_range.add(id_val)

        res += sum(ids_in_range)

    return res


def main():
    do_part_on_input(1, sum_invalid_ids)
    do_part_on_input(2, sum_invalid_ids, extras=True)


if __name__ == "__main__":
    main()
