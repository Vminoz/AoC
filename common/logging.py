import sys
from pathlib import Path
from sys import argv
from time import perf_counter
from typing import Callable, Literal, TypeAlias, cast

from .ansi import (
    BG_WHITE,
    BLINK,
    BRIGHT_BLUE,
    BRIGHT_YELLOW,
    GREEN,
    ITALIC,
    MAGENTA,
    RED,
    RST,
    Ansi,
)
from .ansi import (
    highlight as h,
)

Level: TypeAlias = Literal["i", "v", "u"]
LEVEL_MAP: dict[Level, int] = {"i": 1, "v": 2, "u": 3}
LEVEL_FMT = {1: [BRIGHT_YELLOW, BLINK], 2: [BRIGHT_BLUE], 3: [MAGENTA]}


class TheLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TheLogger, cls).__new__(cls)

            # options
            cls._instance._level = 1
            cls._instance._rich = True
            cls._instance._timestamp_lv = 1
            cls._instance._clear_on_message = False
            cls._instance._wait_on_message = False

            # state
            cls._latest_was_message = False

            cls._instance.lap()
        return cls._instance

    @property
    def is_verbose(self) -> bool:
        return self._level > 1

    @property
    def is_debug(self) -> bool:
        return self._level > 2

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = self.valid_level(value)

    @property
    def rich(self) -> bool:
        """Note: Only applies to leveled logs"""
        return self._rich

    @rich.setter
    def rich(self, value: bool):
        self._rich = value

    @property
    def clear_on_message(self) -> bool:
        return self._clear_on_message

    @clear_on_message.setter
    def clear_on_message(self, value: bool):
        self._clear_on_message = value

    @property
    def wait_on_message(self) -> bool:
        return self._wait_on_message

    @wait_on_message.setter
    def wait_on_message(self, value: bool):
        self._wait_on_message = value

    @property
    def timestamp_lv(self) -> int:
        return self._timestamp_lv

    @timestamp_lv.setter
    def timestamp_lv(self, value: str | int):
        self._timestamp_lv = int(value)

    @staticmethod
    def valid_level(value: str | int) -> int:
        if isinstance(value, str):
            if value in LEVEL_MAP:
                return LEVEL_MAP[cast(Level, value)]
            msg = f"Invalid level flag {value=}"
            raise ValueError(msg)
        if value not in LEVEL_FMT:
            print("Invalid log level, defaulting to info")
            return 1
        return value

    def m(self, message: str, ts: bool = False, end: str = "\n"):
        if not self.rich:
            return
        if self.clear_on_message:
            if not self._latest_was_message:
                Ansi.clear_screen()
            Ansi.top_left()
            self._latest_was_message = True
        if ts:
            self.log_time()
        print(Ansi.fmt(message, [RED], [BRIGHT_YELLOW]), end=end)
        if self.wait_on_message:
            inp = input(
                Ansi.fmt(
                    h("[continue]") + "|" + h("q") + "uit|" + h("a") + "uto → ",
                    [BLINK],
                    [GREEN],
                )
                + Ansi.e(GREEN)
            )
            Ansi.up(1)
            Ansi.clear_tail()

            if inp == "q":
                sys.exit(0)
            if inp == "a":
                self.wait_on_message = False

    def lap(self):
        self.start_time = perf_counter()

    def fmt_ms(self) -> str:
        t = self.ms()
        return f"{t:.2f} ms" if t < 10_000 else f"{t / 1000:.2f}  s"

    def ms(self) -> float:
        return (perf_counter() - self.start_time) * 1000

    def log_time(self, end=""):
        Ansi.wrap([GREEN], print, self._ts(self.fmt_ms()), end=end)

    @staticmethod
    def _ts(contents: str):
        return f"【{contents:>10}】"

    def log(self, lv: int, *args, _skip_ts: bool = False, **kwargs):
        if lv > self.level:
            return
        if not self.rich:
            print(*args, **kwargs)
            return
        elif not _skip_ts and not self.clear_on_message and lv <= self.timestamp_lv:
            self.log_time()
        Ansi.wrap(LEVEL_FMT[lv], print, *args, **kwargs)
        self._latest_was_message = False

    def i(self, *args, sep: str = " ", end: str = "\n", **kwargs):
        self.log(1, *args, sep=sep, end=end, **kwargs)

    def v(self, *args, sep: str = " ", end: str = "\n", **kwargs):
        self.log(2, *args, sep=sep, end=end, **kwargs)

    def d(self, *args, sep: str = " ", end: str = "\n", **kwargs):
        self.log(3, *args, sep=sep, end=end, **kwargs)

    def bench(self, func: Callable, *args, _n_runs: int = 1000, **kwargs):
        s = 0.0
        part = _n_runs // 50
        with Ansi(MAGENTA, BG_WHITE):
            for i in range(_n_runs):
                if i and not i % part:
                    n = i // part
                    est = f"~{1 + s * (_n_runs - i) / i // 1000:.0f}s"
                    print(" " * n + "█" * (50 - n) + f"{est:>5} ", end="\r")
                self.lap()
                func(*args, **kwargs)
                s += self.ms()
        fmt = Ansi.e(BRIGHT_BLUE, ITALIC)
        comma = RST + ", " + fmt
        print(
            Ansi.fmt(self._ts(f"µ={s / _n_runs:.2f} ms"), [MAGENTA]),
            func.__name__ + "(",
            "".join(
                [
                    fmt,
                    comma.join(a.name if isinstance(a, Path) else str(a) for a in args)
                    + comma * bool(kwargs)
                    + comma.join(f"{RST + k + fmt}={a}" for k, a in kwargs.items()),
                    RST,
                ]
            ),
            ")",
            sep="",
        )

    @staticmethod
    def get_level_from_argv():
        if "-v" in argv:  # Verbose
            return 2
        if "-d" in argv:  # Debug/Display
            return 3
        return 1

    @staticmethod
    def timestamp_lv_from_argv():
        if "-T" in argv:  # timestamp never
            return 0
        if "-t" in argv:  # timestamp on verbose
            return 2
        return 1  # timestamp on info

    @classmethod
    def from_argv(cls):
        logger_instance = cls()
        logger_instance.rich = "-r" not in argv
        logger_instance.timestamp_lv = cls.timestamp_lv_from_argv()
        logger_instance.level = cls.get_level_from_argv()
        logger_instance.clear_on_message = "-c" in argv
        logger_instance.wait_on_message = "-I" in argv
        return logger_instance

    def _one_of_each(self):
        self.i("This is an info message.")
        self.v("This is a verbose message.")
        self.d("This is a debug message.")


if __name__ == "__main__":
    logger = TheLogger.from_argv()
    logger._one_of_each()

    test_logger = TheLogger()
    print("\nNew logger instance is same:", logger is test_logger, end="\n\n")

    for level in LEVEL_MAP:
        print(f"{level=}")
        test_logger.level = test_logger.valid_level(level)
        logger._one_of_each()
        print()
