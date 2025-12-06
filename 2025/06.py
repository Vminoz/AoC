"""--- Day 6: Trash Compactor ---"""

from functools import reduce
from operator import add, mul
from pathlib import Path

from common import do_part_on_input, logger

OP = {"*": mul, "+": add}


def grand_total(filename: str) -> int:
    lines = Path(filename).read_text().split("\n")
    operators = [OP[c] for c in lines[-1].split()]
    buffer = [int(c) for c in lines[0].split()]
    for ln in lines[1:-1]:
        buffer = [operators[i](buffer[i], int(c)) for i, c in enumerate(ln.split())]
    return sum(buffer)


def right_to_left_sum(filename: str) -> int:
    lines = Path(filename).read_text().split("\n")
    operators = lines[-1]
    operands = lines[:-1]
    res = 0
    numbers = []
    for j in range(len(operands[0]) - 1, -1, -1):
        s = reduce(add, (ln[j] for ln in operands if ln[j] != " "), "")
        if s:
            numbers.append(int(s))
        op = operators[j] if j < len(operators) else " "
        if op != " ":
            op_res = reduce(OP[op], numbers)
            res += op_res
            numbers.clear()
            logger.d(op, numbers, "=", op_res)
    return res


def main():
    do_part_on_input(1, grand_total)
    do_part_on_input(2, right_to_left_sum)


if __name__ == "__main__":
    main()
