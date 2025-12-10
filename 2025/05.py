"""--- Day 5: Cafeteria ---"""

from pathlib import Path

from common import do_part_on_input


def count_good_ingredients(filename: str) -> int:
    ranges, ingredients = Path(filename).read_text().split("\n\n")
    good_ranges = parse_ranges(ranges.split("\n"))

    good_ingredients = 0
    for line in ingredients.split("\n"):
        ingredient = int(line)
        if any(ingredient in r for r in good_ranges):
            good_ingredients += 1

    return good_ingredients


def total_good_ingredients(filename: str) -> int:
    good_ranges = parse_ranges(Path(filename).read_text().split("\n\n")[0].split("\n"))
    good_ranges.sort(key=lambda r: r.start)
    merged_ranges = merge_ranges(good_ranges)

    res = 0
    for r in merged_ranges:
        res += r.stop - r.start

    return res


def merge_ranges(ranges: list[range]) -> list[range]:
    merged_ranges: list[range] = []
    for i, r in enumerate(ranges):
        if i == 0 or r.start > merged_ranges[-1].stop:
            merged_ranges.append(r)
            continue
        merged_ranges[-1] = range(
            merged_ranges[-1].start, max(r.stop, merged_ranges[-1].stop)
        )
    return merged_ranges


def parse_ranges(ranges: list[str]) -> list[range]:
    good_ranges = []
    for line in ranges:
        st, ed = (int(e) for e in line.split("-"))
        good_ranges.append(range(st, ed + 1))
    return good_ranges


def main():
    do_part_on_input(1, count_good_ingredients)
    do_part_on_input(2, total_good_ingredients)


if __name__ == "__main__":
    main()
