from collections import deque as DQ
from dataclasses import dataclass


@dataclass
class Coord3d:
    """Just for fun"""

    x: int
    y: int
    z: int
    INDEX = {0: "x", 1: "y", 2: "z"}

    def __iter__(self):
        self._idx = -1
        return self

    def __next__(self):
        if not hasattr(self, "_idx"):
            self._idx = -1
        if self._idx < 2:
            self._idx += 1
            return self[self._idx]
        raise StopIteration

    def __add__(self, other):
        return Coord3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __getitem__(self, idx) -> int:
        return self.__getattribute__(self.INDEX[idx])

    def __setitem__(self, idx, val: int) -> None:
        self.__setattr__(self.INDEX[idx], val)

    def __hash__(self) -> int:
        return hash(tuple(self))

    def neighborhood(self) -> list:
        return [
            Coord3d(self.x + 1, self.y, self.z),
            Coord3d(self.x - 1, self.y, self.z),
            Coord3d(self.x, self.y + 1, self.z),
            Coord3d(self.x, self.y - 1, self.z),
            Coord3d(self.x, self.y, self.z + 1),
            Coord3d(self.x, self.y, self.z - 1),
        ]


class VoxelBody:
    def __init__(
        self,
    ) -> None:
        self.voxels = set()
        self.volume = 0
        self.surface = 0
        self.b_box = [Coord3d(1000, 1000, 1000), Coord3d(-1000, -1000, -1000)]

    def add(self, coord: Coord3d):
        self.volume += 1
        self.surface += 6
        self.voxels.add(coord)
        for i in range(3):
            if coord[i] <= self.b_box[0][i]:
                self.b_box[0][i] = coord[i] - 1
            if coord[i] >= self.b_box[1][i]:
                self.b_box[1][i] = coord[i] + 1
        for n in coord.neighborhood():
            if n in self.voxels:
                self.surface -= 2

    def in_bounding_box(self, coord: Coord3d):
        for i in range(3):
            if coord[i] < self.b_box[0][i]:
                return False
            if coord[i] > self.b_box[1][i]:
                return False
        return True

    def calc_outer_surf(self):
        surf = 0
        seen = {self.b_box[0]}
        positions = DQ([self.b_box[0]])
        while positions:
            pos = positions.pop()
            for n in pos.neighborhood():
                if n in self.voxels:
                    surf += 1
                elif n not in seen and self.in_bounding_box(n):
                    positions.append(n)
                seen.add(n)
        return surf


def main():
    vb = VoxelBody()
    with open("input.txt") as f:
        for line in f:
            line.rstrip()
            c = Coord3d(*(int(n) for n in line.split(",")))
            vb.add(c)
    print("P1:", vb.surface)
    print("P2:", vb.calc_outer_surf())


if __name__ == "__main__":
    main()
