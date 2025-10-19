from common import do_part_on_input, lines, logger


def ranges_offset(range_offsets: list[tuple[range, int]]):
    def f(num: int):
        for r, o in range_offsets:
            if num in r:
                return num + o
        return num

    return f


def lowest_location(filename: str):
    almanac = lines(filename)
    seeds = list(map(int, next(almanac).split()[1:]))
    next(almanac)
    for line in almanac:
        if line[0].isalpha():
            ranges = []
            continue

        if line.isspace():
            logger.v(seeds)
            seeds = list(map(ranges_offset(ranges), seeds))
            continue

        dest, source, length = map(int, line.split())
        ranges.append((range(source, source + length), dest - source))
    return min(map(ranges_offset(ranges), seeds))


def lowest_location_from_ranges(filename: str):
    seeds, *maps = open(filename).read().split("\n\n")
    seeds = list(map(int, seeds.split()[1:]))
    maps = [[list(map(int, line.split())) for line in m.splitlines()[1:]] for m in maps]

    in_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

    out_ranges: list[tuple[int, int]] = []
    for start_range in in_ranges:
        ranges = [start_range]
        logger.v("\n", *start_range)
        new_ranges: list[tuple[int, int]] = []
        for map_range in maps:
            while ranges:
                start_range, end_range = ranges.pop()
                for dest, source, length in map_range:
                    map_rend = source + length
                    if map_rend <= start_range or end_range <= source:
                        continue  # No overlap
                    offset = dest - source
                    if start_range < source:
                        ranges.append((start_range, source))
                        start_range = source
                    if map_rend < end_range:
                        ranges.append((map_rend, end_range))
                        end_range = map_rend
                    new_ranges.append((start_range + offset, end_range + offset))
                    # TODO: Visualize better
                    break
                else:
                    new_ranges.append((start_range, end_range))
            logger.v("\t→", new_ranges)
            ranges = new_ranges
            new_ranges = []
        out_ranges += ranges
    return min(r[0] for r in out_ranges)


def main():
    do_part_on_input(1, lowest_location)
    do_part_on_input(2, lowest_location_from_ranges)


if __name__ == "__main__":
    main()
