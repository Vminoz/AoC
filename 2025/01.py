from common import lines, do_part_on_input, logger


def count_zeros(filename: str, add_laps: bool = False) -> int:
    zeros = 0
    notches = 100
    dial = 50
    already_counted = False
    for i, line in enumerate(lines(filename)):
        ds = line[0]
        d = 1 if ds == "R" else -1
        n = int(line[1:].strip())
        laps, dial = divmod(dial + n * d, notches)
        if add_laps:
            zeros += abs(laps)
            if d == -1:
                zeros += (dial == 0) - already_counted
            already_counted = dial == 0
        elif dial == 0:
            zeros += 1
        logger.d(i, ds, n, dial, zeros)
    return zeros


def main():
    do_part_on_input(1, count_zeros)
    do_part_on_input(2, count_zeros, add_laps=True)


if __name__ == "__main__":
    main()
