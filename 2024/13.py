"""--- Day 13: Claw Contraption ---"""

from typing import TypeAlias

from common import do_part_on_input, logger
from common.input_parsing import re_2d
from common.maths import P2D

MachineSpec: TypeAlias = tuple[P2D, P2D, P2D]  # D_a, D_b, P


COST_A = 3
COST_B = 1
MAX_PRESSES = 100
PRIZE_OFFSET = 10_000_000_000_000


def get_minimum_tokens(ms: MachineSpec, offset: bool) -> int:
    """P1
    min  cTx
    s.t.
        Ax = b
        x >= 0
    where
        x = [N_a; N_b]
        c = [C_a; C_b]
        A = [D_ax D_bx; D_ay, D_by]
        b = [P_x; P_y]
    Unique solution:
        N_a = (P_x D_ay - P_y D_ax) / det
        N_b = (P_y D_bx - P_x D_by) / det
    """
    D_a, D_b, p = ms

    det = D_a[0] * D_b[1] - D_a[1] * D_b[0]
    if det == 0:
        raise ValueError("Matrix is singular, assumption invalid")

    if offset:
        p = p[0] + PRIZE_OFFSET, p[1] + PRIZE_OFFSET

    a = (D_b[1] * p[0] - D_b[0] * p[1]) / det
    b = (D_a[0] * p[1] - D_a[1] * p[0]) / det

    logger.d(a, b, det)
    if a < 0 or b < 0:
        logger.v("too small")
        return 0
    if not offset and (a > MAX_PRESSES or b > MAX_PRESSES):
        logger.v("too big")
        return 0
    if int(a) != a or int(b) != b:
        logger.v("not int")
        return 0
    return int(a) * COST_A + int(b) * COST_B


def fewest_tokens_to_win_all(filename: str, offset: bool = False) -> int:
    machines = read_machines(filename)
    tokens = 0
    for m in machines:
        cost = get_minimum_tokens(m, offset)
        tokens += cost
        if cost:
            logger.v(m, cost, end="\n\n")
    return tokens


def read_machines(filename: str) -> list[MachineSpec]:
    machines = []
    with open(filename) as f:
        machines = [parse_machine(b) for b in f.read().split("\n\n")]
    return machines


def parse_machine(s: str) -> MachineSpec:
    a, b, p = s.splitlines()
    return re_2d(a), re_2d(b), re_2d(p)


def main():
    do_part_on_input(1, fewest_tokens_to_win_all)
    do_part_on_input(2, fewest_tokens_to_win_all, offset=True)


if __name__ == "__main__":
    main()
