"""--- Day 17: Chronospatial Computer ---"""

from collections import deque
from dataclasses import dataclass
from typing import Generator

from common import do_part_on_input, logger
from common.ansi import highlight


@dataclass
class ChronospatialComputer:
    # registers
    a: int
    b: int
    c: int
    # instructions
    program: list[int]
    instruction: int = 0

    @classmethod
    def from_str(cls, s: str):
        li = s.split("\n")
        a, b, c = [int(x.split(": ")[1]) for x in li[:3]]
        program = [int(x) for x in li[4].split(": ")[1].split(",")]
        return cls(a, b, c, program)

    def __post_init__(self):
        self.op = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def __repr__(self):
        progrepr = []
        for i in range(0, len(self.program), 2):
            opr, opd = self.op[self.program[i]], self.program[i + 1]
            r = f"{opr.__name__} {opd}"
            if i == self.instruction:
                r = highlight(r)
            progrepr.append(r)

        return f"\n{self}\n{', '.join(progrepr)}"

    def __str__(self):
        return f"A: {bin(self.a)[2:]}\nB: {bin(self.b)[2:]}\nC: {bin(self.c)[2:]}"

    def eval(self) -> Generator[int, None, None]:
        while self.instruction < len(self.program):
            if logger.is_debug:
                logger.m(repr(self))

            opcode = self.program[self.instruction]
            operation = self.op[opcode]
            operand = self.program[self.instruction + 1]
            output = operation(operand)

            if not output == -2:  # jumped
                self.instruction += 2
            if output and output < 0:
                output = None

            if output is not None:
                if logger.is_debug:
                    logger.m(highlight(f"→ {output}"))
                yield output

    def run(self) -> list[int]:
        out = []
        for o in self.eval():
            out.append(o)
        return out

    def combo_operand(self, operand: int) -> int:
        match operand:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                if operand > 6:
                    raise ValueError(f"Invalid operand {operand}")
                return operand

    def dv(self, operand) -> int:
        """A // 2**cop"""
        return self.a // (1 << self.combo_operand(operand))

    def adv(self, operand: int) -> None:
        """dv -> A"""
        self.a = self.dv(operand)

    def bdv(self, operand: int) -> None:
        """dv -> B"""
        self.b = self.dv(operand)

    def cdv(self, operand: int) -> None:
        """dv -> C"""
        self.c = self.dv(operand)

    def bxl(self, operand: int) -> None:
        """B xor op -> B"""
        self.b ^= operand

    def bxc(self, _: int) -> None:
        """B xor C -> B"""
        self.b ^= self.c

    def bst(self, operand: int) -> None:
        """cop%8 -> B"""
        self.b = self.combo_operand(operand) & 0b111

    def jnz(self, operand: int) -> int:
        """Go to instruction[op] if A == 0"""
        if self.a == 0:
            return -1
        self.instruction = operand
        return -2

    def out(self, operand: int) -> int:
        """cop%8 -> out"""
        return self.combo_operand(operand) & 0b111

    @classmethod
    def self_generate(cls, program: list[int]) -> int:
        """
        Return the lowest A such that the program generates itself.
        Or raise a ValueError.
        ASSUMES:
            A decreases by the same number of bits for each eval until output.
            One output = one pass of full program.
        """
        # test run
        tc = cls(1 << 12, 0, 0, program)
        next(tc.eval())
        bit_shift = 13 - tc.a.bit_length()
        logger.v(f"{bit_shift=}")

        candidates = deque([0])
        logger.v(program)
        while candidates:
            left = candidates.popleft() << bit_shift
            for right in range(1 << bit_shift):  # try all A&(bs-1)
                a = left + right
                out = cls(a, 0, 0, program).run()
                if out == program[-len(out) :]:
                    # output matches tail
                    logger.v(a, out)
                    candidates.append(a)
                if out == program:
                    return a

        raise ValueError("No solution found")


def test_computer():
    c = ChronospatialComputer(0, 0, 9, [2, 6])
    out = c.run()
    assert c.b == 1

    c = ChronospatialComputer(10, 0, 0, [5, 0, 5, 1, 5, 4])
    out = c.run()
    assert out == [0, 1, 2]

    c = ChronospatialComputer(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    out = c.run()
    assert out == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0] and c.a == 0

    c = ChronospatialComputer(0, 29, 0, [1, 7])
    out = c.run()
    assert c.b == 26

    c = ChronospatialComputer(0, 2024, 43690, [4, 0])
    out = c.run()
    assert c.b == 44354


def run_machine(filename: str) -> str:
    with open(filename) as f:
        csc = ChronospatialComputer.from_str(f.read())
    logger.v(repr(csc))
    return ",".join(map(str, csc.run()))


def find_self_gernerating_program(filename: str) -> int:
    with open(filename) as f:
        csc = ChronospatialComputer.from_str(f.read())
    program = csc.program
    seed = ChronospatialComputer.self_generate(program)
    return seed


def main():
    test_computer()
    do_part_on_input(1, run_machine)
    do_part_on_input(2, find_self_gernerating_program)


if __name__ == "__main__":
    main()
