"""--- Day 21: Keypad Conundrum ---"""

from common import do_part_on_input, lines, logger

DPAD = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]
NPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]


def deconstruct_keypad(keypad: list[list[str]]) -> dict[tuple[str, str], str]:
    movements = {}
    for i, r in enumerate(keypad):
        for j, k in enumerate(r):
            if k == " ":
                continue
            for ni, nr in enumerate(keypad):
                for nj, nk in enumerate(nr):
                    if nk == " ":
                        continue
                    di, dj = ni - i, nj - j
                    up = (di < 0) * -di * "^"
                    down = (di > 0) * di * "v"
                    left = (dj < 0) * -dj * "<"
                    right = (dj > 0) * dj * ">"

                    # move ordered by distance to A in DPAD
                    movements[(k, nk)] = left + down + up + right + "A"

                    # Hard-coded overrides for avoiding the non-key states
                    if k in "741" and nk in "0A":
                        movements[(k, nk)] = right + down + "A"
                    elif nk in "741" and k in "0A":
                        movements[(k, nk)] = up + left + "A"
                    elif k == "<":
                        movements[(k, nk)] = right + up + "A"
                    elif nk == "<":
                        movements[(k, nk)] = down + left + "A"

    logger.d(keypad, "\n→", movements)
    return movements


DPAD_MAP = deconstruct_keypad(DPAD)
NPAD_MAP = deconstruct_keypad(NPAD)


def replay(seq: str, depth: int) -> str:
    layers = depth + 1
    state = [(0, 2)] * depth + [(3, 2)]
    mv = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    buff = [""] * layers
    for k in seq:
        if k in mv:
            state[0] = (state[0][0] + mv[k][0], state[0][1] + mv[k][1])
            for i in range(layers):
                buff[i] += " "
            continue
        ns = [" "] * layers
        for i in range(layers):
            keypad = NPAD if i == depth else DPAD
            dk = keypad[state[i][0]][state[i][1]]
            ns[i] = dk
            if dk in mv:
                state[i + 1] = (
                    state[i + 1][0] + mv[dk][0],
                    state[i + 1][1] + mv[dk][1],
                )
                break
        for i in range(layers):
            buff[i] += ns[i]
    logger.d(len(seq))
    return seq + "\n" + "\n".join(buff)


def code_keypresses(code: str, depth: int) -> str:
    logger.v(code)
    dcode = input_code(code, NPAD_MAP)
    for _ in range(depth):
        dcode = input_code(dcode, DPAD_MAP)
    if logger.is_debug:
        m = replay(dcode, depth)
        logger.m(m)
    return dcode


def input_code(code: str, keymap: dict[tuple[str, str], str]) -> str:
    pk, seq = "A", ""
    for k in code:
        # go to key and press A
        seq += keymap[(pk, k)]
        pk = k
    return seq


def sum_complexities(filename: str, depth: int = 2) -> int:
    if depth > 15:
        msg = f"Depth {depth} would take ages, let's not"
        raise ValueError(msg)
    codes = [line.rstrip() for line in lines(filename)]
    cs = 0
    for code in codes:
        cs += int(code[:-1]) * len(code_keypresses(code, depth))
    return cs


def just_sum_complexities(filename: str, depth: int = 25) -> int:
    codes = [line.rstrip() for line in lines(filename)]
    dpad_dist = {k: len(v) for k, v in DPAD_MAP.items()}
    logger.v("map", DPAD_MAP)
    logger.v("fp", {k: input_code(v, DPAD_MAP) for k, v in DPAD_MAP.items()})
    logger.v(dpad_dist, end="\n\n")
    for _ in range(depth - 1):
        dpad_dist = {
            k: 1
            if k[0] == k[1]
            else (
                dpad_dist[("A", v[0])]
                + sum(dpad_dist[(vk, v[i + 1])] for i, vk in enumerate(v[:-1]))
            )
            for (k, v) in DPAD_MAP.items()
        }
        logger.d(dpad_dist, end="\n\n")

    cs = 0
    for code in codes:
        dpad0 = input_code(code, NPAD_MAP)
        logger.v(code, dpad0)
        seqlen = dpad_dist[("A", dpad0[0])]
        logger.d("A", dpad0[0], seqlen)
        for i, k in enumerate(dpad0[:-1]):
            nk = dpad0[i + 1]
            steps = dpad_dist[(k, nk)]
            logger.d(k, nk, steps)
            seqlen += steps
        logger.v(seqlen)
        cs += int(code[:-1]) * seqlen
    return cs


def main():
    do_part_on_input(1, sum_complexities)
    do_part_on_input(2, just_sum_complexities)


if __name__ == "__main__":
    main()
