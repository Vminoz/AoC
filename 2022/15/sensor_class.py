import re

import numpy as np


class Sensor:
    def __init__(self, sx: int, sy: int, bx: int, by: int) -> None:
        self.sx = sx
        self.sy = sy
        self.bx = bx
        self.by = by
        self.man_range: int = manhattan_2d((sx, sy), (bx, by))
        self._inside = set()
        self._outside = set()
        self._bounds = (-np.inf, np.inf)

    def __str__(self) -> str:
        return f"{self.sx, self.sy} ~ {self.bx, self.by}"

    def __getitem__(self, i):
        return (self.sx, self.sy, self.bx, self.by)[i]

    def __hash__(self) -> int:
        return hash((self.sx, self.sy))

    def __contains__(self, pos) -> bool:
        if self.inside:
            return pos in self.inside
        return (
            self._in_bounds(pos)
            and manhattan_2d((self.sx, self.sy), pos) < self.man_range
        )

    def add_bounds(self, lb: int, ub: int):
        self._bounds = (lb, ub)
        self._inside = {i for i in self._inside if lb < i[0] < ub and lb < i[1] < ub}
        self._outside = {i for i in self._outside if lb < i[0] < ub and lb < i[1] < ub}
        print(self._inside, self._outside)

    def _in_bounds(self, pos: tuple[int, int]) -> bool:
        return (
            self._bounds[0] < pos[0] < self._bounds[1]
            and self._bounds[0] < pos[1] < self._bounds[1]
        )

    def get_x_interval(self, y: int) -> list:
        dy = abs(self.sy - y)
        budget = self.man_range - dy
        return [] if budget < 0 else [self.sx - budget, self.sx + budget]

    @property
    def inside(self) -> set[tuple[int, int]]:
        if self._inside:
            return self._inside
        for i in range(self.man_range + 1):
            for j in range(self.man_range + 1 - i):
                for d in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    pos = (self.sx + d[0] * i, self.sy + d[1] * j)
                    if self._in_bounds(pos):
                        self._inside.add(pos)
        return self._inside

    @property
    def outside(self) -> set[tuple[int, int]]:
        if self._outside:
            return self._outside
        for i in range(self.man_range + 2):
            j = self.man_range - i + 1
            for d in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                pos = (self.sx + d[0] * i, self.sy + d[1] * j)
                if self._in_bounds(pos):
                    self._outside.add((self.sx + d[0] * i, self.sy + d[1] * j))
        return self._outside


def manhattan_2d(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def parse_sensors(file_name: str) -> set[Sensor]:
    numbers = re.compile(r"-?\d+")
    sensors = set()
    with open(file_name) as f:
        for line in f:
            nums = [int(num) for num in numbers.findall(line)]
            sensors.add(Sensor(*nums))
    return sensors
