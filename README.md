# AOC - Vminoz
Solutions for [Advent of Code](https://adventofcode.com)

Mainly Python so far, 2023 and 2024 with only standard library and with a total runtime < 1min per calendar on my phone.
2022 had each day in a separate folder instead, the idea was to isolate the days but having common logging and visuals was more fun.

## Structure
```sh
.
├── {year}
│   ├── inputs  # Input txt files by day
│   │   ├── {day}.txt   # Personal
│   │   ├── {day}s.txt  # Short
│   │   └── {day}e.txt  # Extra
│   └── {day}.py  # Day-solution
├── common  # Import module for common code
│   ├── __init__.py
│   ├── ansi.py
│   ├── input_parsing.py
│   ├── logging.py
│   ├── maths.py
│   └── visuals.py
├── vis  # Separate visualizations ─ when the terminal isn't enough
│   ├── v'%d'.py  # Day-specific script
│   └── reqs.txt  # Requirements for ./vis
├── meta  # Scripts for downloading inputs
│   ├── startday.py
│   └── template.py.tt
├── shell  # Terminal utilities
│   ├── doday   # Bash wrapper for meta.startday, calls `code` on output
│   ├── runall    # Bash script to run all solutions
│   └── aliases   # useful aliases
├── Makefile   # Useful phonies
└── README.md  # 📍 You are here
```

> Note: 2022 doesn't follow the standard year directory structure and has dependencies listed in `2022/requirements.txt`.

## Setup
##### Recommended:
```sh
make install  # pre-commit hook
make shortcut >> ~/.bashrc  # or ~/.zshrc, create aoc alias
```

## Visuals
Some days have a _nice_ animation if run in verbose or debug mode, look for `logger.m(`, e.g.
```sh
rg 'logger\.m' --files-with-matches | rg -o '\d+' | sort
```
To see these:
```sh
sol <day> -v -c -I
# -v:verbose
# -d:debug
# -c:clear on draw
# -I:interactive
```

## {year}/vis
These scripts have their dependencies listed with [Inline script metadata](https://peps.python.org/pep-0723/).
Run them with `uv run`.
