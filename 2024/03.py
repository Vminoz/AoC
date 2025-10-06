"""--- Day 3: Mull It Over ---"""

import re

from common import do_part_on_input, lines

mul = re.compile(r"(?:do(?:n't)?\(\)|mul\((\d{1,3}),(\d{1,3})\))")


def sum_mults(filename: str, dodonts: bool = False):
    tot = 0
    enable = True
    for line in lines(filename):
        for m in mul.finditer(line):
            if line[m.start()] == "d":
                enable = (not dodonts) or (m.group(0) == "do()")
                continue
            if enable:
                op1, op2 = m.groups()
                tot += int(op1) * int(op2)
    return tot


def main():
    do_part_on_input(1, sum_mults)
    do_part_on_input(2, sum_mults, dodonts=True)


if __name__ == "__main__":
    main()
