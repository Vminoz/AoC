"""--- Day 7: Bridge Repair ---"""

import math
from operator import add, mul
from typing import Callable, TypeAlias

from common import do_part, lines, logger, parse_input_with

MaskedEquation: TypeAlias = list[int]
MaskedEquations: TypeAlias = list[MaskedEquation]
IntOp: TypeAlias = Callable[[int, int], int]


def get_equations(filename: str) -> MaskedEquations:
    """[*[result, *ops]]"""
    eqs = []
    for line in lines(filename):
        res, *ops = line.rstrip().split()
        res = res.rstrip(":")
        eqs.append([int(i) for i in (res, *ops)])
    return eqs


def get_tot_calibration_result(
    equations: MaskedEquations,
    ops: tuple[IntOp, ...] = (add, mul),
) -> int:
    tot = 0
    for eq in equations:
        res = get_res_if_possible(eq, ops)
        tot += res
        if logger.is_verbose:
            logger.m(f"{'✅' if res else '❌'} {eq[0]}={'█'.join(map(str,eq[1:]))}")
    return tot


def int_concat(a: int, b: int) -> int:
    """Slightly faster casting to str and back"""
    if b == 0:
        return a * 10
    return a * 10 ** (int(math.log10(b)) + 1) + b


def get_res_if_possible(eq: MaskedEquation, operators: tuple[IntOp, ...]) -> int:
    res, first, *remaining = eq
    values = [first]
    for y in remaining:
        values = [op(x, y) for x in values for op in operators]
    return res if res in values else 0


def main():
    eqs = parse_input_with(get_equations)
    do_part(1, get_tot_calibration_result, eqs)
    do_part(2, get_tot_calibration_result, eqs, (add, mul, int_concat))


if __name__ == "__main__":
    main()
