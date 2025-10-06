"""--- Day 24: Crossed Wires ---"""

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property, reduce
from operator import add, and_, or_, xor
from pathlib import Path
from typing import ClassVar, TypeAlias

from common import do_part_on_input, lines, logger
from common.input_parsing import USE_SMALL_FILE

OPS = {
    "AND": and_,
    "OR": or_,
    "XOR": xor,
}

Gates: TypeAlias = dict[str, tuple[str, str, str]]
Wires: TypeAlias = dict[str, int]


def is_output(wire: str):
    return wire[0] == "z"


def is_input(wire: str):
    return wire[0] in "xy"


@dataclass(frozen=True)
class LogicalBit:
    reg: str
    pos: int

    @cached_property
    def btype(self):
        return (
            "in" if is_input(self.reg) else "out" if is_output(self.reg) else self.reg
        )

    @classmethod
    def from_wire(cls, w: str):
        return cls(reg=w[0], pos=int(w[1:]) if w[1:].isdigit() else -3)


@dataclass(frozen=True)
class BadBit:
    inputs: "tuple[LogicalBit | BadBit, LogicalBit | BadBit]"
    operator: str

    btype: ClassVar[str] = "B"

    @cached_property
    def pos(self):
        return -2 if any(i.btype == "B" for i in self.inputs) else -1


def read_wires_gates(filename: str) -> tuple[Wires, Gates]:
    wires = {}
    gates = {}
    reading_values = True
    for line in lines(filename):
        line = line.rstrip()
        if not line:
            reading_values = False
            continue
        if reading_values:
            wire, value = line.split(": ")
            wires[wire] = int(value)
        else:
            w1, op, w2, _, out = line.split(" ")
            gates[out] = (w1, w2, op)
    return wires, gates


def evaluate(wires: Wires, gates: Gates) -> Wires:
    wires = wires.copy()
    opq = deque((*v, k) for k, v in gates.items())
    while opq:
        w1, w2, op, out = opq.popleft()
        if w1 in wires and w2 in wires:
            v1, v2 = wires[w1], wires[w2]
            v = OPS[op](v1, v2)
            logger.d(w1, v1, w2, v2, op, "->", v)
            wires[out] = v
        else:
            opq.append((w1, w2, op, out))
    return wires


def collect(bits: Iterable[int]) -> int:
    """Collect bits LE and return the int"""
    return sum(b << i for i, b in enumerate(bits))


def evaluate_circuit(filename: str) -> int:
    wires, gates = read_wires_gates(filename)
    wires = evaluate(wires, gates)
    logger.v(wires)

    z_wires = sorted(k for k in wires if k.startswith("z"))
    bits = [wires[w] for w in z_wires]
    if logger.is_verbose:
        logger.v(
            " ".join(reversed(z_wires)),
            "   ".join(reversed([str(b) for b in bits])),
            sep="\n",
        )

    return collect(bits)


def find_corrections(gates: Gates) -> list[tuple[str, str]]:
    """
    Notes:
        The circuit is a broken ripple carry adder:
        https://upload.wikimedia.org/wikipedia/commons/8/85/RippleCarry2.gif
        So we need to make sure LSBs pass a valid HA and the rest is lifted through FAs.
    Approach:
        Try to build a ripple carry and find the right gate to swap when mismatch.
    """
    given_n_swaps = 4
    corrs: list[tuple[str, str]] = []
    while len(corrs) < given_n_swaps:
        swap = get_swap(gates)
        if swap:
            corrs.append(swap)
            # apply swap
            a, b = swap
            gates[a], gates[b] = gates[b], gates[a]

    # write to file for visualization, ugly but ok
    with open(Path(__file__).parent / "vis" / "24.txt", "w") as file:
        file.write("\n")
        for o, (w1, w2, op) in gates.items():
            file.write(f"{w1} {op} {w2} -> {o}\n")

    return corrs


def get_swap(gates: Gates) -> tuple[str, str]:
    expressions = {logical_expr(out_wire, gates): out_wire for out_wire in gates}
    if logger.is_debug:
        for k, v in expressions.items():
            logger.d(v, k)
    for ex, ow in expressions.items():
        ob = LogicalBit.from_wire(ow)
        if isinstance(ex, BadBit):
            if ob.btype != "out" or ex.pos != -1:
                continue
            e1, e2 = ex.inputs
            if ex.operator == "XOR":
                w1, w2, _ = gates[ow]
                other_wire = {expr: wire for expr, wire in zip((e1, e2), (w2, w1))}
                if LogicalBit("C", ob.pos) in (e1, e2):
                    return (
                        other_wire[LogicalBit("C", ob.pos)],
                        expressions[LogicalBit("X", ob.pos)],
                    )
                if LogicalBit("X", ob.pos) in (e1, e2):
                    return (
                        other_wire[LogicalBit("X", ob.pos)],
                        expressions[LogicalBit("C", ob.pos)],
                    )
        elif ex.reg == "S" and ow != f"z{ex.pos:02d}":
            return ow, f"z{ex.pos:02d}"
    msg = f"No swap found on {len(expressions)} expressions!"
    raise ValueError(msg)


def logical_expr(wire: str, gates: Gates) -> LogicalBit | BadBit:
    if is_input(wire):
        return LogicalBit.from_wire(wire)
    w1, w2, op = gates[wire]
    e1, e2 = logical_expr(w1, gates), logical_expr(w2, gates)
    if e1.btype != "B" and e2.btype != "B" and e1.pos == e2.pos:
        bitpos = e1.pos
        types = {e1.btype, e2.btype}
        if types == {"in"}:
            if op == "AND":
                return (
                    LogicalBit("C", 1)
                    if bitpos == 0  # HA
                    else LogicalBit("A", bitpos)
                )
            if op == "XOR":
                return LogicalBit("X" if bitpos > 0 else "S", bitpos)
        elif types == {"C", "X"}:
            if op == "AND":
                return LogicalBit("I", bitpos)  # Inner
            if op == "XOR":
                return LogicalBit("S", bitpos)
        elif types == {"A", "I"} and op == "OR":
            return LogicalBit("C", bitpos + 1)  # Carry out
    return BadBit((e1, e2), op)


def correct_circuit(filename: str) -> str:
    _, gates = read_wires_gates(filename)
    swaps = reduce(add, find_corrections(gates))
    return ",".join(sorted(swaps))


def main():
    do_part_on_input(1, evaluate_circuit)
    if USE_SMALL_FILE:
        logger.i("P2: <invalid on non-personal input>")
    else:
        do_part_on_input(2, correct_circuit)


if __name__ == "__main__":
    main()
