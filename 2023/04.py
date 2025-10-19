from collections import defaultdict

from common import do_part_on_input, lines, logger


def cards_reader(file: str):
    for i, line in enumerate(lines(file)):
        yield i + 1, *map(set, map(str.split, line.strip().split(": ")[1].split(" | ")))


def card_points(filename: str):
    points = 0
    for _, winners, nums in cards_reader(filename):
        if matches := winners & nums:
            points += 1 << (len(matches) - 1)
    return points


def card_count(filename: str):
    cards = defaultdict(lambda: 1)
    for i, winners, nums in cards_reader(filename):
        dupes = cards[i]
        if matches := winners & nums:
            for j in range(len(matches)):
                cards[i + j + 1] += dupes
        if logger.level > 1:
            logger.v(dict(cards.items()))
    return sum(cards.values())


def main():
    do_part_on_input(1, card_points)
    do_part_on_input(2, card_count)


if __name__ == "__main__":
    main()
