"""--- Day 5: Print Queue ---"""

from collections import defaultdict
from typing import Callable, Generator

from common import do_part_on_input, lines, logger


def get_rules(
    filename: str,
) -> tuple[defaultdict[str, set], Generator[str, None, None]]:
    i_lines = lines(filename)
    must_be_before: defaultdict[str, set[str]] = defaultdict(lambda: set())
    for line in i_lines:
        line = line.rstrip()
        if not line:
            return must_be_before, i_lines
        before, after = line.split("|")
        must_be_before[after].add(before)
    raise ValueError("no blank line")


def mid_page_if_correct(must_be_before: dict[str, set], pages: list[str]) -> int:
    banned = set()
    for page in pages:
        if page in banned:
            return 0
        banned |= must_be_before[page]

    return int(pages[len(pages) // 2])


def mid_page_if_restored(must_be_before: dict[str, set], pages: list[str]) -> int:
    has_moved = False
    would_move: dict[str, str] = {}
    np = len(pages)

    for i in range(np):
        page = pages[i]

        if page in would_move:
            swap_page = would_move[page]
            logger.d(would_move)
            logger.v("reinserting", page, "before", swap_page)
            pages.insert(pages.index(swap_page), pages.pop(i))
            logger.d(pages)

            has_moved = True
            for op in must_be_before[page]:
                if would_move.get(op) == swap_page:
                    would_move[op] = page

        for op in must_be_before[page]:
            if op not in would_move:
                would_move[op] = page

    if not has_moved:
        return 0
    return int(pages[np // 2])


def sum_middle_pages(filename: str, pagelist_func: Callable = mid_page_if_correct):
    must_be_before, rem_lines = get_rules(filename)
    res = 0
    for line in rem_lines:
        line = line.rstrip()
        logger.v(line)
        res += pagelist_func(must_be_before, line.split(","))
    return res


def main():
    do_part_on_input(1, sum_middle_pages)
    do_part_on_input(2, sum_middle_pages, pagelist_func=mid_page_if_restored)


if __name__ == "__main__":
    main()
