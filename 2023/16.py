from itertools import product
from typing import TypeAlias

from common import P2D, do_part_on_input, logger

Beam: TypeAlias = tuple[int, int, int, int]

BARS = {"|": "|", "-": "─", "\\": "⟍", "/": "⟋"}

MIRROR = {
    "⟍": (lambda di, dj: (dj, di)),
    "⟋": (lambda di, dj: (-dj, -di)),
}

SPLIT = {
    "|": (0, 1, ((1, 0), (-1, 0))),
    "─": (1, 0, ((0, 1), (0, -1))),
}


class BeamBox:
    def __init__(self, tiles: list[str]) -> None:
        self.tiles = tiles
        self.ri = range(len(tiles))
        self.rj = range(len(tiles[0]))
        self._init_features()
        self.memo = {}

    def _init_features(self) -> None:
        self.mirrors = set()
        self.splitters = set()
        for i, j in product(self.ri, self.rj):
            tile = self.tiles[i][j]
            if tile in MIRROR:
                self.mirrors.add((i, j))
            elif tile in SPLIT:
                self.splitters.add((i, j))

    @classmethod
    def from_file(cls, filename: str):
        tiles = open(filename).read()
        for b in BARS:
            tiles = tiles.replace(b, BARS[b])
        tiles = tiles.split("\n")
        return cls(tiles)

    def run_beam(self, start_beam: Beam):
        energized = set()
        used_starts = set()
        beams = [start_beam]
        while beams:
            logger.v("Beams:", beams)
            b = beams.pop()
            if b in self.memo:
                logger.v("From Memo")
                energy, new_beams = self.memo[b]
            else:
                energy, new_beams = self.sub_beam(b)
                self.memo[b] = energy, new_beams
            beams.extend(nb for nb in new_beams if nb not in used_starts)
            used_starts.add(b)
            energized |= energy
            if logger.level > 2:
                self.show_beams(energized, energy)
        if logger.level > 1:
            self.show_beams(energized)
        return energized

    def sub_beam(self, b: Beam):
        energy = set()
        visited = set()
        i, j, di, dj = b
        while i in self.ri and j in self.rj and (i, j, di, dj) not in visited:
            visited.add((i, j, di, dj))
            energy.add((i, j))
            if (i, j) in self.splitters:
                si, sj, new_ds = SPLIT[self.tiles[i][j]]
                if si * di + sj * dj:
                    return energy, [(i, j, *d) for d in new_ds]

            if (i, j) in self.mirrors:
                di, dj = MIRROR[self.tiles[i][j]](di, dj)

            i += di
            j += dj
        return energy, []

    def show_beams(self, energized: set[P2D], newly_energized: set[P2D] | None = None):
        if newly_energized is None:
            newly_energized = set()
        jmax = self.rj.stop
        message = ["【┌" + "─" * jmax + "┐】"]
        for i, r in enumerate(self.tiles):
            line = "【│】"
            for j, c in enumerate(r):
                if (i, j) in newly_energized:
                    line += "【█】"
                elif (i, j) in energized:
                    line += "【" + c + "】"
                else:
                    line += c
            message.append(line + "【│】")
        message.append(f"【└{len(energized):─<{jmax}}┘】")
        logger.m("\n".join(message))

    def get_edge_beams(self) -> list[Beam]:
        return [
            *((i, 0, 0, 1) for i in self.ri),  # →
            *((i, self.rj.stop - 1, 0, -1) for i in self.ri),  # ←
            *((0, j, 1, 0) for j in self.rj),  # ↓
            *((self.ri.stop - 1, j, -1, 0) for j in self.rj),  # ↑
        ]

    def max_energy(self):
        current = 0
        for b in self.get_edge_beams():
            logger.v("START BEAM", b)
            n_energ = len(self.run_beam(b))
            if n_energ > current:
                current = n_energ
        return current


def energize(filename: str):
    beam_box = BeamBox.from_file(filename)
    energized = beam_box.run_beam((0, 0, 0, 1))
    return len(energized)


def energize_all(filename: str):
    beam_box = BeamBox.from_file(filename)
    return beam_box.max_energy()


def main():
    do_part_on_input(1, energize)
    do_part_on_input(2, energize_all)


if __name__ == "__main__":
    main()
