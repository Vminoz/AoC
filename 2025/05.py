"""--- Day 5: Cafeteria ---"""

from common import lines, do_part_on_input


def part1(filename: str) -> int:
    at_ingredients = False
    good_ranges = []
    good_ingredients = 0
    for line in lines(filename):
        ln = line.strip()
        if not at_ingredients:
            if not ln:
                at_ingredients = True
                continue
            st, ed = (int(e) for e in ln.split("-"))
            good_ranges.append(range(st, ed + 1))
            continue
        ingredient = int(ln)
        if any(ingredient in r for r in good_ranges):
            good_ingredients += 1

    return good_ingredients


def main():
    do_part_on_input(1, part1)
    # do_part_on_input(2, ???)


if __name__ == "__main__":
    main()
