from sys import argv
from typing import Any, Callable, ParamSpec, TypeVar

from .ansi import CODES as ANSICODES
from .ansi import Ansi
from .input_parsing import argv_input_file, lines
from .logging import TheLogger
from .maths import P2D, P3D, tuple_ranges

T = TypeVar("T")
P = ParamSpec("P")


# Instantiate logger and input file from cli arguments
# NOTE: cli arguments are undocumented, .input_parsing and .logging just pick them up
logger = TheLogger.from_argv()


def skip_part(part) -> bool:
    return f"-{part}" in argv


def do_part_on_input(
    part: int,
    sol: Callable[..., int | str],
    filename: str = "",
    **kwargs: Any,
):
    """sol: (filename:str, **kwargs) -> int"""
    if skip_part(part):
        return
    if not filename:
        input_file = argv_input_file()
        if input_file is None:
            raise ValueError("no input file")
        logger.d(f"{sol.__name__}('{input_file}')")
        filename = input_file
    label_call(f"P{part}", True, True, sol, filename, **kwargs)


def do_part(part: int, sol: Callable[P, int | str], *args: P.args, **kwargs: P.kwargs):
    if skip_part(part):
        return
    label_call(f"P{part}", True, True, sol, *args, **kwargs)


def parse_input_with(parser: Callable[[str], T]) -> T:
    """parser: (filename:str) -> T"""
    input_file = argv_input_file()
    if input_file is None:
        raise ValueError("no input file")
    return label_call("Parsed", False, False, parser, input_file)


def label_call(
    label: str,
    always: bool,
    with_result: bool,
    func: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    logger.lap()
    res = func(*args, **kwargs)
    if always or logger.is_verbose:
        if with_result:
            logger.i(f"{label}: {res}")
        else:
            logger.i(label)
    return res


__all__ = (
    "Ansi",
    "argv_input_file",
    "ANSICODES",
    "lines",
    "logger",
    "P2D",
    "P3D",
    "TheLogger",
    "tuple_ranges",
)
