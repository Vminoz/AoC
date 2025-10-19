# Originally solved in spreadsheets with a bunch of cell references and
#   =LET(pairs,REGEXEXTRACT($C2,REGEXREPLACE($C2,"(\d+ "&F$1&")","($1)")),
#    MAX(MAP(pairs, lambda(p,VALUE(LEFT(p, LEN(p) - 2))))))
# P1:
#   =SUM(MAP(A:A, LAMBDA(x, LET(nums,
#    REGEXREPLACE(x,"[^\d]",""),VALUE(LEFT(nums) & RIGHT(nums))))))
# P2:
#   =SUM(MAP(A:A, LAMBDA(x, LET(converted,
#    SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(
#    x,"one","o1e"),"two","t2"),"three","t3e"),"four","4"),"five","5e"),"six","6"),"seven","7"),"eight","e8"),"nine","9"),
#    nums, REGEXREPLACE(converted,"[^\d]",""),VALUE(LEFT(nums) & RIGHT(nums))))))
import re
from math import prod

from common import do_part_on_input, lines

BAG = {
    "r": 12,
    "g": 13,
    "b": 14,
}
RD = r"(\d+)"


def p1(filename: str):
    res = 0
    for line in lines(filename):
        game, sets = line.split(": ")
        for color, n in BAG.items():
            if max(int(m.group(1)) for m in re.finditer(RD + f" {color}", sets)) > n:
                break
        else:
            res += int(game[5:])
    return res


def p2(filename: str):
    return sum(
        prod(
            max(int(m.group(1)) for m in re.finditer(RD + f" {color}", line))
            for color in BAG
        )
        for line in lines(filename)
    )


def main():
    do_part_on_input(1, p1)
    do_part_on_input(2, p2)


if __name__ == "__main__":
    main()
