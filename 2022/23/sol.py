from collections import deque as DQ

from matplotlib import pyplot as plt

EIGHT2D = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
)
MASKS = ((0, 1, 2), (4, 5, 6), (0, 7, 6), (2, 3, 4))  # NSWE


def parse_elves(file_name: str) -> set:
    elves = set()
    with open(file_name) as f:
        for i, line in enumerate(f):
            for j, ch in enumerate(line):
                if ch == "#":
                    elves.add((i, j))
    return elves


def move_elf(elf: tuple[int, int], elves: set, order: DQ):
    nbs = [(elf[0] + d[0], elf[1] + d[1]) for d in EIGHT2D]
    nb_elf = [p in elves for p in nbs]
    if not any(nb_elf):
        return elf
    for mask in order:
        if all(not nb_elf[i] for i in mask):
            return nbs[mask[1]]
    return elf


def step_elves(elves: set, order: DQ, verbose: bool = False) -> tuple[set, bool]:
    moves = {}  # To: From
    moving = False
    for elf in elves:
        new_pos = move_elf(elf, elves, order)
        if not moving and new_pos != elf:
            moving = True
        if new_pos in moves:
            if verbose:
                print("Two going to", new_pos, "none will")
            other_elf = moves.pop(new_pos)
            moves[other_elf] = other_elf
            moves[elf] = elf
        else:
            moves[new_pos] = elf
            if verbose:
                print(elf, "→", new_pos)
    return set(moves), moving


def bounding_rect_area(some_set: set) -> tuple[int, int]:
    max_i = max(some_set, key=lambda e: e[0])[0]
    min_i = min(some_set, key=lambda e: e[0])[0]
    max_j = max(some_set, key=lambda e: e[1])[1]
    min_j = min(some_set, key=lambda e: e[1])[1]
    return (max_i - min_i + 1) * (max_j - min_j + 1)


def show_elves(elves):
    e_x, e_y = [], []
    for elf in elves:
        e_x.append(elf[1])
        e_y.append(-elf[0])
    plt.scatter(e_x, e_y, c="r")
    plt.axis("off")
    plt.show()


def main():
    elves = parse_elves("input.txt")
    show_elves(elves)
    prio_order = DQ(MASKS)
    moving = True
    cnt = 0
    while moving:
        cnt += 1
        elves, moving = step_elves(elves, prio_order)
        prio_order.rotate(-1)
        if cnt == 10:
            print("P1:", bounding_rect_area(elves) - len(elves))
        if not cnt % 10:
            print(cnt, end="\r")
    print("P2:", cnt)
    show_elves(elves)


if __name__ == "__main__":
    main()
