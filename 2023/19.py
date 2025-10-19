import re
from dataclasses import dataclass
from math import prod
from operator import gt, lt
from typing import Literal

from common import do_part_on_input, logger

OP = {"<": lt, ">": gt}

RE_DIGITS = re.compile(r"(\d+)")


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_str(cls, string):
        return cls(*map(int, RE_DIGITS.findall(string)))

    def __getitem__(self, key):
        return self.__getattribute__(key)

    @property
    def rating(self):
        return self.x + self.m + self.a + self.s


@dataclass
class Stage:
    atr: str
    op: Literal["<", ">"]
    ref: int
    out: str

    def apply(self, part: Part):
        return self.out if OP[self.op](part[self.atr], self.ref) else None


class Workflow:
    def __init__(self, stages: list[Stage], default: str) -> None:
        self.stages = stages
        self.default = default

    def apply(self, part: Part):
        for stage in self.stages:
            out = stage.apply(part)
            if out is not None:
                return out
        return self.default


class System:
    def __init__(self, workflows: list[str]) -> None:
        self.workflows: dict[str, Workflow] = {}
        for r in workflows:
            wf, s = r.rstrip("}").split("{")
            str_stages = s.split(",")
            stages: list[Stage] = []
            for step in str_stages[:-1]:
                cond, out = step.split(":")
                op = ">" if ">" in step else "<"
                atr, ref = cond.split(op)
                stages.append(Stage(atr, op, int(ref), out))
            self.workflows[wf] = Workflow(stages, str_stages[-1])

    def process_part(self, part: Part) -> int:
        wf = "in"
        while wf not in "AR":
            wf = self.workflows[wf].apply(part)
        return part.rating if wf == "A" else 0

    def exhaust(self):
        idx = {"x": 0, "m": 1, "a": 2, "s": 3}
        states = [("in",) + ((1, 4001),) * 4]
        total = 0
        while states:
            wf, *lims = states.pop()

            if wf == "R":
                continue
            logger.v(f"\n{wf + ' ':─<79}┤")

            if wf == "A":
                value = prod(lim[1] - lim[0] for lim in lims)
                logger.v(lims, "→", value)
                total += value
                continue

            self._split_on_workflow(idx, states, wf, lims)
        return total

    def _split_on_workflow(self, idx: dict, states: list, wf: str, lims: list):
        workflow = self.workflows[wf]
        for stage in workflow.stages:
            ref = stage.ref
            out = stage.out
            atr_i = idx[stage.atr]
            bound = lims[atr_i]
            if stage.op == "<":
                if bound[0] > ref:
                    continue
                out_bnd = (bound[0], min(ref, bound[1]))
                stay_bnd = (max(ref, bound[0]), bound[1])
            elif stage.op == ">":
                if bound[1] < ref:
                    continue
                stay_bnd = (bound[0], min(ref + 1, bound[1]))
                out_bnd = (max(ref + 1, bound[0]), bound[1])
            out_lims = lims.copy()
            out_lims[atr_i] = out_bnd
            lims[atr_i] = stay_bnd
            states.append((out, *out_lims))
            logger.v(f"{out}: {out_lims}\nstay: {lims}\n")

        states.append((workflow.default, *lims))

        if logger.level > 2:
            logger.log(3, f"\n{'┌':─<10}STATES", "\n".join(map(str, states)), sep="\n")


def split_input(filename: str) -> list[list[str]]:
    return [block.split("\n") for block in open(filename).read().split("\n\n")]


def sum_accepted(filename: str):
    workflows, parts = split_input(filename)
    parts = [Part.from_str(p) for p in parts]
    workflows = System(workflows)
    return sum(map(workflows.process_part, parts))


def count_acceptable(filename: str):
    workflow = System(split_input(filename)[0])
    return workflow.exhaust()


def main():
    do_part_on_input(1, sum_accepted)
    do_part_on_input(2, count_acceptable)


if __name__ == "__main__":
    main()
