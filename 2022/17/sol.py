import numpy as np


class NotTetris:
    ROCKS = [  # Rocks ordered bottom cell to top
        tuple((i, 0) for i in range(4)),  # _
        ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),  # -|-
        ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),  # _|
        tuple((0, i) for i in range(4)),  # |
        ((0, 0), (1, 0), (0, 1), (1, 1)),  # ⊞
    ]

    def __init__(self, width: int) -> None:
        self.rock_i = 0
        self.blocks = {(i, 0) for i in range(width)}
        self.width = width
        self.height = 0
        self.block_height = 0
        self.popped_height = 0
        self.active_rock = None

    def __str__(self) -> str:
        not_tetris_string = ""
        for y in reversed(range(self.height + 1)):
            if not y:
                return f"{not_tetris_string}+" + "-" * self.width + "+"
            row = "|"
            for x in range(self.width):
                if (x, y) in self.blocks or (
                    self.active_rock is not None
                    and (self.active_rock == (x, y)).all(axis=1).any()
                ):
                    row += "█"
                else:
                    row += "░"
            not_tetris_string += row + "|\n"

    def _new_rock(self, i):
        self.active_rock = np.array(NotTetris.ROCKS[i])
        self.active_rock += (2, self.height + 4)

    def step(self, jet: int):
        new_pos = self.active_rock + (jet, 0)
        self.move(new_pos)

        new_pos = self.active_rock - (0, 1)
        self.move(new_pos, True)

    def move(self, new_pos, stopping=False) -> bool:
        for cell in new_pos:
            if not 0 <= cell[0] < self.width:
                return True
            if tuple(cell) in self.blocks:
                if stopping:
                    self.blocks |= {tuple(c) for c in self.active_rock}
                    self.block_height = max(self.block_height, self.active_rock[-1, 1])
                    self.active_rock = None
                return True
        self.active_rock = new_pos
        self.height = max(self.block_height, self.active_rock[-1, 1])
        return False

    def simulate(
        self, jets: list, n_rocks: float, manual: bool = False, probe: int = 2022
    ) -> int:
        self.jets = jets
        self.manual = manual
        ji, _ = 0, len(jets)
        ri, nr = 0, len(NotTetris.ROCKS)
        cache = {}
        for rock_count in range(int(n_rocks)):
            if rock_count == probe:
                print(f"{probe} rocks; height:", self.height)

            # Try to find cycle
            key = ri, ji
            if rock_count > probe and key in cache:
                rc, h = cache[key]
                cycle_length = rock_count - rc
                num_cycles, overshoot = divmod(n_rocks - rock_count, cycle_length)
                if not overshoot:
                    tot_h = int(self.height + num_cycles * (self.height - h))
                    print(
                        f"Found nice cycle of length {cycle_length} after "
                        + f"the {rock_count}:th rock (h:{self.height}).\n"
                        + f"Skipping {num_cycles:.0} cycles for remaining height.."
                        + f"\n{n_rocks:.0} rocks; height: {tot_h}"
                    )
                    return tot_h
            else:
                cache[key] = rock_count, self.height

            # Actually simulate
            self._new_rock(ri)
            ri = (ri + 1) % nr
            ji = self._drop_active(ji)

            if not self.manual and not rock_count % 10_000:
                print(f"Dropped rock {rock_count:_}", end="\r")
        print(f"Dropped rock {ri:_}")
        return self.height

    def _drop_active(self, ji):
        while self.active_rock is not None:
            j = self.jets[ji]
            if self.manual:
                print(self)
                self.manual = not input(
                    f"Jet: {chr(j + 61)}, step? (not blank → skip) "
                )
            self.step(j)
            ji = (ji + 1) % len(self.jets)
        return ji


def main():
    with open("input.txt") as f:
        jets = [ord(ch) - 61 for ch in f.read()]
    nt = NotTetris(7)
    nt.simulate(jets, 1e12, True)


if __name__ == "__main__":
    main()
