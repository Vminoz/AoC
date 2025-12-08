"""--- Day 8: Playground ---"""

from math import sqrt, prod

from common import P3D, lines, do_part_on_input, logger
from common.input_parsing import USE_SMALL_FILE


class JunctionBoxConnections:
    def __init__(self, boxes: list[P3D]) -> None:
        self.boxes = boxes

        self.unconnected = set(range(len(boxes)))
        # Map of circuit id to list of jbox indices
        self.circuits: dict[int, set[int]] = {}
        # Map of jbox indices to circuit id
        self.jbc_map: dict[int, int] = {}
        self.distances = sorted(calc_distances(self.boxes), reverse=True)
        logger.d(*self.distances, sep="\n")

    @classmethod
    def from_csv(cls, filename: str):
        return cls(
            [tuple(int(i) for i in line.strip().split(",")) for line in lines(filename)]  # type: ignore
        )

    def connect_pair(self, a: int, b: int) -> None:
        if circ_a := self.jbc_map.get(a):
            if circ_b := self.jbc_map.get(b):
                if circ_a == circ_b:
                    logger.d(a, "and", b, "both in", circ_a, "nothing new")
                    return  # Do nothing
                else:
                    self._merge_circuits(circ_a, circ_b)
            else:
                self._connect_box(b, circ_a)
        elif circ_b := self.jbc_map.get(b):
            self._connect_box(a, circ_b)
        else:
            new_circ_id = self.boxes[a][0]
            while new_circ_id in self.circuits:
                new_circ_id *= 10
            self.circuits[new_circ_id] = set()
            self._connect_box(a, new_circ_id)
            self._connect_box(b, new_circ_id)

    def _merge_circuits(self, circ_a: int, circ_b: int) -> None:
        b_circuit = self.circuits.pop(circ_b)
        self.circuits[circ_a] |= b_circuit
        for box in b_circuit:
            self.jbc_map[box] = circ_a
        logger.d("merged circuits", circ_a, "and", circ_b)

    def _connect_box(self, box_index: int, circuit_id: int) -> None:
        logger.d(box_index, "added to", circuit_id)
        self.jbc_map[box_index] = circuit_id
        self.circuits[circuit_id].add(box_index)
        self.unconnected.remove(box_index)

    def connect_closest_pair(self) -> tuple[int, int]:
        if not self.distances:
            raise ValueError("Tried to connect more than there are jbox pairs")
        _dist, a, b = self.distances.pop()
        self.connect_pair(a, b)
        if logger.is_debug:
            logger.m(f"{self.boxes[a]!s:<15} ─── {self.boxes[b]}")
        return a, b

    def connect_all(self) -> tuple[P3D, P3D]:
        while self.unconnected or len(self.circuits) > 1:
            a, b = self.connect_closest_pair()
        return self.boxes[a], self.boxes[b]


def dist(a: P3D, b: P3D) -> float:
    return sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def calc_distances(points: list[P3D]) -> list[tuple[float, int, int]]:
    return [
        (dist(a, points[j]), i, j)
        for i, a in enumerate(points)
        for j in range(i + 1, len(points))
    ]


def part1(filename: str, cables: int) -> int:
    connections = JunctionBoxConnections.from_csv(filename)
    for i in range(cables):
        connections.connect_closest_pair()
        logger.v(i, "circuits:", connections.circuits)
    return prod(sorted(len(c) for c in connections.circuits.values())[-3:])


def part2(filename: str) -> int:
    connections = JunctionBoxConnections.from_csv(filename)
    last_a, last_b = connections.connect_all()
    return last_a[0] * last_b[0]


def main():
    do_part_on_input(1, part1, cables=10 if USE_SMALL_FILE else 1000)
    do_part_on_input(2, part2)


if __name__ == "__main__":
    main()
