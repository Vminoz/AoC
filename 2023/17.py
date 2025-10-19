from heapq import heappop

from common import do_part_on_input, lines, logger


def turn(d: complex):
    if d.real:
        return (-1j, 1j)
    if d.imag:
        return (-1, 1)
    raise ValueError("Why did we stop?")


def crucible_djikstra(filename: str, move_range: range = range(1, 4)):
    blocks: dict[complex, int] = {
        i + j * 1j: int(cost)
        for i, line in enumerate(lines(filename))
        for j, cost in enumerate(line.strip())
    }
    target = max(blocks, key=abs)
    best = {}
    states: list[tuple[int, int, complex, tuple[int, ...]]] = [
        (0, 0, 1 + 0j, (0,)),
        (0, 1, 1j, (0,)),
    ]
    i = 1  # insertion order (for heappop to behave on equal cost)
    while states:
        cost, _, delta, path = heappop(states)
        pos = path[-1]

        if pos == target:
            if logger.level > 1:
                show_path(path, target)
            return cost

        for d in turn(delta):
            c, p = cost, path
            for step in range(1, move_range.stop):
                npos = p[-1] + d
                if npos not in blocks:
                    break
                p += (npos,)
                c += blocks[npos]
                i += 1
                if step < move_range.start:
                    continue
                k = (npos, d)
                if k not in best or c < best[k]:
                    best[k] = c
                    states.append((c, i, d * step, p))

    return str(target)


def show_path(p: tuple[int, ...], tgt: complex):
    ri = range(int(tgt.real) + 1)
    rj = range(int(tgt.imag) + 1)
    path = {(int(z.real), int(z.imag)) for z in p}
    lines = []
    for i in ri:
        line = ""
        for j in rj:
            if i + j * 1j == tgt:
                line += "【█】"
            elif (i, j) in path:
                line += "█"
            else:
                line += "."
        lines.append(line)
    logger.m("\n".join(lines))


def main():
    do_part_on_input(1, crucible_djikstra)
    do_part_on_input(2, crucible_djikstra, move_range=range(4, 11))


if __name__ == "__main__":
    main()
