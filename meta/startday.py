import json
import re
import sys
import webbrowser
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from common.ansi import GREEN, ITALIC, MAGENTA, RED, Ansi


def print_info(msg: str):
    """Print message to stderr as to not pipe to stdout"""
    sys.stderr.write(Ansi.fmt(f"{msg}", [MAGENTA]))


def print_success(msg: str):
    sys.stderr.write(Ansi.fmt(f"✅ {msg}\n", [GREEN]))


def print_err(msg: str):
    sys.stderr.write(Ansi.fmt(f"❌ {msg}\n", [RED]))


URL = "https://adventofcode.com/"

SECRETS_FILE = Path("--secrets.json")

if not SECRETS_FILE.exists():
    print_info(
        f"No {SECRETS_FILE!s} found, create interactively by opening your browser? [y]/n\n → "
    )
    if input().lower() not in ("y", ""):
        sys.exit(1)
    webbrowser.open(URL)
    print_info(
        "Navigate to an inputs page and check your request header for Cookie 'session'\n"
        " → session="
    )
    cookie = input().strip()
    SECRETS_FILE.write_text(json.dumps({"COOKIE": cookie}, indent=2))

SECRETS = json.loads(SECRETS_FILE.read_text())
COOKIE = SECRETS["COOKIE"]
LEADERBOARD_ID = SECRETS.get("LEADERBOARD_ID", "")
TEMPLATE = Path("meta/template.py.tt").read_text()

RE_DAY_TITLE = re.compile(r"--- .*? ---")


def get_input_web(year: int, day: int) -> str:
    headers = {"cookie": "session=" + COOKIE}
    input_getter = URL + f"{year}/day/{day}/input"
    request = Request(input_getter, headers=headers)
    try:
        with urlopen(request) as response:
            input_data: str = response.read().decode("utf-8")
        return input_data.rstrip()
    except HTTPError as e:
        print_err(f"{e.code}: {e.reason} ({input_getter})")
    except URLError as e:
        print_err(f"Failed to connect to the server: {e.reason}")
    return ""


def extract_info(day: int) -> dict[str, str]:
    info = {}
    headers = {"cookie": "session=" + COOKIE}
    input_getter = URL + f"day/{day}"
    anchor = "example:</p>\n<pre><code>"
    anchor_end = "</code></pre>"
    request = Request(input_getter, headers=headers)
    try:
        with urlopen(request) as response:
            day_page: str = response.read().decode("utf-8")

        title = RE_DAY_TITLE.search(day_page)
        if title is not None:
            info["title"] = title.group(0)

        ap = day_page.find(anchor)
        ae = day_page.find(anchor_end)
        if ap != -1 and ae != -1:
            info["example"] = day_page[ap + len(anchor) : ae].strip()

    except HTTPError as e:
        print_err(f"{e.code}: {e.reason} ({input_getter})")
    except URLError as e:
        print_err(f"Failed to connect to the server: {e.reason}")

    return info


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "day",
        nargs="?",
        type=int,
        help="(int) Day to fetch and template, defaults to today.",
        default=datetime.today().day,
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        help="year of date, defaults to current year.",
        default=datetime.today().year,
    )
    parser.add_argument(
        "--no-browser", "-n", action="store_true", help="(flag) don't open in browser."
    )
    args = parser.parse_args()
    day = args.day
    year = args.year
    no_browser = args.no_browser

    problem_input_str = get_input_web(year, day)
    if not problem_input_str:
        print_err(f"Failed to fetch input for day {day}")
        sys.exit(1)
    day_info = extract_info(day)
    if not day_info:
        print_err("Failed to fetch info...")

    year_folder = Path(str(year))
    sol_file = year_folder / f"{day:>02}.py"
    if not sol_file.exists():
        start_content = ""
        if title := day_info.get("title"):
            start_content += f'"""{title}"""\n\n'
        start_content += TEMPLATE
        sol_file.write_text(start_content)

    # Personal input
    inputs = year_folder / "inputs"
    inputs.mkdir(exist_ok=True)

    problem = inputs / (f"{day:>02}.txt")
    problem.write_text(problem_input_str)

    # A bit more tricky to automate getting (e.g. isn't always the first code block),
    #   but just copy when reading instructions
    sample = inputs / (f"{day:>02}s.txt")
    sample.write_text(day_info.get("example", ""))

    print_success(
        f"Created files for day {day}\n"
        "ℹ️ Writing filenames to stdout for so they can be passed to an editor"
        " e.g. " + Ansi.fmt("code . (...)", [ITALIC, MAGENTA])
    )
    print(f"{sol_file.absolute()} {problem.absolute()} {sample.absolute()}")

    if not no_browser:
        if LEADERBOARD_ID:
            webbrowser.open(URL + f"{year}/leaderboard/private/view/{LEADERBOARD_ID}")
        webbrowser.open(URL + f"{year}/day/{day}")


if __name__ == "__main__":
    main()
