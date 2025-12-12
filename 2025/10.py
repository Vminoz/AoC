"""--- Day 10: Factory ---"""

from collections import deque as DQ
from dataclasses import dataclass

from common import do_part_on_input, lines, logger
from common.linalg import LinearSystem


@dataclass
class Machine:
    target: int
    buttons: tuple[int, ...]
    joltage: tuple[int, ...]

    def __post_init__(self):
        # Check assumptions
        assert all(self.buttons)

    @classmethod
    def from_string(cls, s: str) -> "Machine":
        s = s.strip()
        tgt_s, *btns_s, jtg_s = s.split()

        tgt = 0
        for c in tgt_s[-1:0:-1]:
            tgt = (tgt << 1) + (c == "#")

        btn = []
        for btns in btns_s:
            btn.append(sum(1 << int(c) for c in btns[1:-1].split(",")))

        jtg = [int(c) for c in jtg_s[1:-1].split(",")]

        instance = cls(tgt, tuple(btn), tuple(jtg))
        logger.d(s, "\n→", instance)
        return instance

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"\ntarget={bin(self.target)},"
            f"\nbuttons=({', '.join(bin(b) for b in self.buttons)}),"
            f"\njoltage={self.joltage}\n)"
        )

    def get_presses_to_target(self) -> list[int]:
        """
        Return _a_ smallest sequence of button presses needed to go from 0 to target
        """
        if self.target == 0:
            return []
        q: DQ[tuple[int, int, list[int]]]  # current_value, press_count, buttons_pressed
        q = DQ([(0, 0, [])])
        visited = {0}

        while q:
            v, c, p = q.popleft()
            if v == self.target:
                return p

            for i, b in enumerate(self.buttons):
                nv = v ^ b

                if nv not in visited:
                    visited.add(nv)
                    q.append((nv, c + 1, p + [i]))
        raise ValueError("Target unreachable?")

    @property
    def button_matrix(self) -> list[list[int]]:
        return [[(b >> i) & 1 for b in self.buttons] for i in range(len(self.joltage))]

    def get_presses_to_joltage(self) -> tuple[int, tuple[int, ...]]:
        """
        Solves Ax = b where A is the button matrix, b is the joltage vector,
        and x is the number of presses per button.
        """
        a = self.button_matrix
        b = list(self.joltage)
        x = LinearSystem(a, b).solve()
        return sum(x), x


def part1(filename: str) -> int:
    res = sum(
        len(Machine.from_string(line).get_presses_to_target())
        for line in lines(filename)
    )
    return res


def part2(filename: str) -> int:
    res = 0
    for i, line in enumerate(lines(filename), start=1):
        np, presses = Machine.from_string(line).get_presses_to_joltage()
        res += np
        logger.v(np, presses, f"{i}: {line}", sep="\t")
    return res


def main():
    do_part_on_input(1, part1)
    do_part_on_input(2, part2)


if __name__ == "__main__":
    main()
