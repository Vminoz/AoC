# Originally solved in spreadsheets with
# P1:
#   =SUM(MAP(A:A, LAMBDA(x, LET(nums,
#    REGEXREPLACE(x,"[^\d]",""),VALUE(LEFT(nums) & RIGHT(nums))))))
# P2:
#   =SUM(MAP(A:A, LAMBDA(x, LET(converted,
#    SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(
#    x,"one","o1e"),"two","t2"),"three","t3e"),"four","4"),"five","5e"),"six","6"),"seven","7"),"eight","e8"),"nine","9"),
#    nums, REGEXREPLACE(converted,"[^\d]",""),VALUE(LEFT(nums) & RIGHT(nums))))))
import re

from common import lines, do_part_on_input

NOT_DIGIT = re.compile(r"[^\d]")


def left_right(s: str):
    return s[0] + s[-1]


def p1(filename: str):
    return sum(map(lambda x: int(left_right(NOT_DIGIT.sub("", x))), lines(filename)))


def p2(filename: str):
    return sum(
        map(
            lambda x: int(left_right(NOT_DIGIT.sub("", cursed_digits(x)))),
            lines(filename),
        )
    )


def cursed_digits(s: str):
    return (
        s.replace("one", "o1e")
        .replace("two", "t2")
        .replace("three", "t3e")
        .replace("four", "4")
        .replace("five", "5e")
        .replace("six", "6")
        .replace("seven", "7")
        .replace("eight", "e8")
        .replace("nine", "9")
    )


def main():
    do_part_on_input(1, p1)
    do_part_on_input(2, p2)


if __name__ == "__main__":
    main()
