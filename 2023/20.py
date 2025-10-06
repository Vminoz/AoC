from math import prod
from functools import reduce
from common import lines, logger, do_part_on_input
from common.maths import lcm
from collections import deque as DQ


class Pulser:
    sent = {0: 0, 1: 0}
    pulses: DQ[tuple["Pulser", "Pulser", int]] = DQ()
    target: str = ""

    def __init__(self, name: str, module_type: str, source: "Pulser"):
        self.listeners: list["Pulser"] = []
        self.state = 0
        self.source_name = source.name

        if module_type == "%":
            self.process = self._flipflop
        elif module_type == "&":
            self.process = self._conjunct
            self.mem = {}
        else:
            self.process = self._pass_through

        self.module_type = module_type
        self.name = name
        self.connect(source)

    def connect(self, source: "Pulser"):
        if self.module_type == "&":
            self.mem[source.name] = 0
        source.listeners.append(self)

    def __repr__(self) -> str:
        if self.module_type == "&":
            s = (
                "".join(k + str(v) for k, v in self.mem.items())
                + "─"
                + ("0" if all(self.mem.values()) else "1")
            )
        else:
            s = self.state
        return f"{self.module_type}{self.name} ─{s}→ " + ",".join(
            _.name for _ in self.listeners
        )

    def _flipflop(self, signal: int, _: "Pulser"):
        if signal == 0:
            self.state = int(not self.state)
            return self.state
        else:
            return -1

    def _conjunct(self, signal: int, source: "Pulser"):
        self.mem[source.name] = signal
        return 0 if all(self.mem.values()) else 1

    def _pass_through(self, signal: int, _: "Pulser"):
        self.state = signal
        return signal

    def pulse(self, signal: int, source: "Pulser"):
        signal = self.process(signal, source)
        if signal < 0:
            return
        logger.log(3, self)
        for rec in self.listeners:
            self.pulses.append((self, rec, signal))
            self.sent[signal] += 1

    @classmethod
    def propagate(cls):
        hits = []
        while cls.pulses:
            source, dest, signal = cls.pulses.popleft()
            dest.pulse(signal, source)
            if signal and dest.name == cls.target:
                hits.append(source.name)
        return hits

    @classmethod
    def reset(cls):
        cls.sent = {0: 0, 1: 0}
        cls.pulses: DQ[tuple["Pulser", "Pulser", int]] = DQ()


class Button(Pulser):
    name = "Button"

    def __init__(self) -> None:
        self.listeners: list["Pulser"] = []

    def press_n(self, n: int):
        for _ in range(n):
            self.press()

    def press(self):
        self.dispatch_signals()
        hits = Pulser.propagate()
        if logger.level > 2:
            logger.m(str(Pulser.sent))
        return hits

    def dispatch_signals(self):
        for rec in self.listeners:
            Pulser.sent[0] += 1
            Pulser.pulses.append((self, rec, 0))

    def connect(self, pulser: Pulser) -> None:
        self.listeners.append(pulser)

    def __str__(self) -> str:
        children = DQ(self.listeners)
        string = []
        while children:
            child = children.popleft()
            if str(child) in string:
                continue
            string.append(str(child))
            children.extend(child.listeners)
        return "\n".join(string)


def read_modules(filename: str):
    modules = {}
    for line in lines(filename):
        id_, str_listeners = line.strip().split(" -> ")
        listeners = [i.lstrip("%&") for i in str_listeners.split(", ")]
        modules[id_.lstrip("%&")] = id_[0], listeners
    return modules


def initialize_pulsers(modules: dict[str, tuple[str, list[str]]]):
    button = Button()
    _, listeners = modules["broadcaster"]
    connections = [(Pulser("broadcaster", "", button), listeners)]
    pulsers: dict[str, Pulser] = {}
    while connections:
        parent, listeners = connections.pop()
        for rec in listeners:
            if rec not in modules:
                pulsers[rec] = Pulser(rec, "", parent)
                continue

            if rec in pulsers:
                pulsers[rec].connect(parent)
                continue

            m_type, sub_listeners = modules[rec]
            pulsers[rec] = Pulser(rec, m_type, parent)
            connections.append((pulsers[rec], sub_listeners))

    Pulser.reset()
    return button, pulsers


def part1(filename: str, presses: int = 1000):
    modules = read_modules(filename)
    button, _ = initialize_pulsers(modules)
    logger.v(button)
    button.press_n(presses)
    logger.v(Pulser.sent)
    return prod(Pulser.sent.values())


def fewest_pulses_to_rx(filename: str):
    modules = read_modules(filename)
    button, pulsers = initialize_pulsers(modules)
    if "rx" not in pulsers:
        return "N/A"
    rx = pulsers[pulsers["rx"].source_name]
    rx_parent_periods = {v.name: 0 for v in pulsers.values() if rx in v.listeners}
    Pulser.target = rx.name
    cnt = 0
    while cnt < 1e6:
        cnt += 1
        hits = button.press()
        if not hits:
            continue

        for h in hits:
            if not rx_parent_periods[h]:
                rx_parent_periods[h] = cnt
                logger.v(rx_parent_periods)

        if all(rx_parent_periods.values()):
            return reduce(lcm, rx_parent_periods.values())

    raise ValueError(f"Couldnt find all frequencies {rx_parent_periods}")


def main():
    do_part_on_input(1, part1)
    do_part_on_input(2, fewest_pulses_to_rx)


if __name__ == "__main__":
    main()
