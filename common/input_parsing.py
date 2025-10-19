import re
from functools import cache
from pathlib import Path
from sys import argv
from typing import Generator

import __main__

RE_NUM = re.compile(r"-?\d+")

USE_SMALL_FILE = "-s" in argv


@cache
def argv_input_file() -> str | None:
    if "-i" in argv:
        next_arg = argv.index("-i") + 1
        if next_arg >= len(argv):
            raise SyntaxError("-i must be followed by a filename")
        file = Path(argv[next_arg])
        check_file(file)
        return str(file)

    return get_input_file(USE_SMALL_FILE)


def get_input_file(small=True) -> str | None:
    if not hasattr(__main__, "__file__"):
        return None
    main_file = Path(__main__.__file__)
    if not main_file.stem.isdigit():
        return None
    file = Path(
        str(main_file.parent / "inputs" / main_file.stem)
        + ("s" if small else "")
        + ".txt"
    )
    check_file(file)
    return str(file)


def check_file(file: Path):
    if not file.is_file():
        raise FileNotFoundError(f"Didn't find {file}")


def lines(problem_input: Path | str) -> Generator[str, None, None]:
    """Yields lines from file"""
    with open(problem_input) as f:
        yield from f


def re_2d(s: str) -> tuple[int, int]:
    n = [int(m) for m in RE_NUM.findall(s)]
    return n[0], n[1]


def re_4d(s: str) -> tuple[int, int, int, int]:
    n = [int(m) for m in RE_NUM.findall(s)]
    return n[0], n[1], n[2], n[3]
