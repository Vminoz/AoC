from typing import Callable

ESC = "\x1b["
RST = "\x1b[0m"

# Styles
BOLD = "1"
DIM = "2"
ITALIC = "3"
UNDERLINE = "4"
BLINK = "5"
REVERSE = "7"
HIDDEN = "8"
STRIKETHROUGH = "9"
DOUBLE_UNDERLINE = "21"

# Foreground text colors
BLACK = "30"
RED = "31"
GREEN = "32"
YELLOW = "33"
BLUE = "34"
MAGENTA = "35"
CYAN = "36"
WHITE = "37"

# Background colors
BG_BLACK = "40"
BG_RED = "41"
BG_GREEN = "42"
BG_YELLOW = "43"
BG_BLUE = "44"
BG_MAGENTA = "45"
BG_CYAN = "46"
BG_WHITE = "47"

# Bright foreground text colors
BRIGHT_BLACK = "90"
BRIGHT_RED = "91"
BRIGHT_GREEN = "92"
BRIGHT_YELLOW = "93"
BRIGHT_BLUE = "94"
BRIGHT_MAGENTA = "95"
BRIGHT_CYAN = "96"
BRIGHT_WHITE = "97"

# Bright background colors
BG_BRIGHT_BLACK = "100"
BG_BRIGHT_RED = "101"
BG_BRIGHT_GREEN = "102"
BG_BRIGHT_YELLOW = "103"
BG_BRIGHT_BLUE = "104"
BG_BRIGHT_MAGENTA = "105"
BG_BRIGHT_CYAN = "106"
BG_BRIGHT_WHITE = "107"

CODES = {
    name: code
    for name, code in globals().items()
    if name.isupper() and name not in ("ESC", "RST")
}

HIGHLIGHT_START = "⟦"
HIGHLIGHT_END = "⟧"


def highlight(text: str) -> str:
    return HIGHLIGHT_START + text + HIGHLIGHT_END


class Ansi:
    def __init__(self, *codes, clear_line=True):
        self.codes = codes
        self.clear = clear_line

    def __enter__(self):
        self.start(*self.codes)

    def __exit__(self, *_):
        self.end()
        if self.clear:
            self.clear_tail()

    @staticmethod
    def e(*codes):
        return f"{ESC}{';'.join(codes)}m"

    @staticmethod
    def clear_tail():
        print(ESC + "K", end="")

    @staticmethod
    def up(n: int):
        print(ESC + str(n) + "A", end="\r")

    @staticmethod
    def clear_screen():
        print(ESC + "2J", end="")

    @staticmethod
    def save_cursor():
        print(ESC + "s", end="")

    @staticmethod
    def restore_cursor():
        print(ESC + "u", end="")

    @staticmethod
    def top_left():
        print(ESC + "H", end="")

    @classmethod
    def start(cls, *codes):
        print(cls.e(*codes), end="")

    @classmethod
    def end(cls):
        print(RST, end="")

    @classmethod
    def fmt(cls, s: str, codes: list[str], highlight: list[str] | None = None):
        ctr = cls.e(*codes)
        if highlight:
            h = cls.e(*highlight)
            s = s.replace(HIGHLIGHT_START, RST + h).replace(HIGHLIGHT_END, RST + ctr)
        return ctr + s + RST

    @classmethod
    def wrap(cls, codes: list[str], func: Callable, *args, **kwargs):
        with cls(*codes):
            func(*args, **kwargs)


if __name__ == "__main__":
    for name, value in CODES.items():
        with Ansi(value):
            print(f"{name:<20}", end="")
        print(f"{value:>3}")

    with Ansi(BG_BRIGHT_BLACK, BLINK, MAGENTA):
        print("Have fun!")
