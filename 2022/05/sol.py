from collections import deque
from re import compile as re_c

MULTIMOVE = True


def parse_box_row(piles: dict[int:deque], line: str):
    for i, pile in piles.items():
        label = line[1 + (i - 1) * 4]
        if not label.isspace():
            pile.appendleft(label)


def pop_n(dq: deque, n: int):
    return (dq.pop() for _ in range(n))


def apply_instruction(piles: dict[int:deque], n: int, fr: int, to: int):
    otherpile = deque(pop_n(piles[fr], n)) if MULTIMOVE else piles[fr]
    piles[to].extend(pop_n(otherpile, n))


def print_piles(piles: dict[int:deque]):
    print("".join(piles[i + 1][-1] if piles[i + 1] else "_" for i in range(len(piles))))


def main():
    re_num = re_c(r"\d+")
    with open("input.txt", "r") as f:
        at_instructions = False
        for i, line in enumerate(f):
            if not i:
                piles = {i + 1: deque() for i in range(len(line) // 4)}
            if not at_instructions:
                if line.isspace():
                    at_instructions = True
                elif line[1] != "1":
                    parse_box_row(piles, line)
                continue
            instruction = (int(m) for m in re_num.findall(line))
            apply_instruction(piles, *instruction)
    # print_piles(piles)


if __name__ == "__main__":
    main()
