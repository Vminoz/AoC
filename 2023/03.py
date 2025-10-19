from dataclasses import dataclass, field

from common import do_part, lines, logger, parse_input_with


@dataclass
class Schematic:
    items: dict[tuple[int, int], str] = field(default_factory=dict)
    parts: set[tuple[int, int]] = field(default_factory=set)
    gears: set[tuple[int, int]] = field(default_factory=set)


def frame_indices(i, j, length):
    yield (i, j - length)
    yield (i, j + 1)
    for k in range(-length, 2):
        yield (i - 1, j + k)
        yield (i + 1, j + k)


def read_schematic(filename: str) -> Schematic:
    schematic = Schematic()
    for i, line in enumerate(lines(filename)):
        parse_schematic_line(schematic, i, line)
    return schematic


def parse_schematic_line(schematic: Schematic, i: int, line: str):
    current_num = ""
    for j, ch in enumerate(line):
        if ch in "0123456789":
            current_num += ch
            continue

        if current_num:
            schematic.items[(i, j - 1)] = current_num
            current_num = ""

        if ch not in ".\n":
            schematic.parts.add((i, j))
            if ch == "*":
                schematic.gears.add((i, j))


def sum_numbers_with_part(schematic: Schematic):
    total = 0
    for k, v in schematic.items.items():
        if isinstance(k, str):
            continue
        if has_part(k, v, schematic.parts):
            total += int(v)
        else:
            logger.v(f"NP {k}")
    return total


def has_part(pos: tuple[int, int], v: str, parts: set):
    logger.v(pos)
    for i_j in frame_indices(*pos, len(v)):
        logger.v(f"\t{i_j}")
        if i_j in parts:
            return True
    return False


def get_parts(pos: tuple[int, int], v: str, parts: set):
    logger.v(pos)
    res = set()
    for i_j in frame_indices(*pos, len(v)):
        logger.v(f"\t{i_j}")
        if i_j in parts:
            res.add(i_j)
    return res


def sum_gear_ratios(schematic: Schematic):
    gear_ratios = {g: [0, 1] for g in schematic.gears}

    for k, v in schematic.items.items():
        if isinstance(k, str):
            continue
        for g in get_parts(k, v, schematic.gears):
            gear_ratios[g][0] += 1
            gear_ratios[g][1] *= int(v)

    total = 0
    for cnt, ratio in gear_ratios.values():
        if cnt != 2:
            continue
        total += ratio

    return total


def main():
    schematic = parse_input_with(read_schematic)
    do_part(1, sum_numbers_with_part, schematic)
    do_part(2, sum_gear_ratios, schematic)


if __name__ == "__main__":
    main()
