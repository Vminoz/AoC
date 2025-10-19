import numpy as np

DIRECTIONS = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}


def update_tail(rope: np.ndarray):
    for n in range(1, rope.shape[0]):
        distance: np.ndarray = rope[n - 1] - rope[n]
        if (abs(distance) > 1).any():
            rope[n] += distance.clip(-1, 1)


def simulate_rope(rope_len):
    rope = np.zeros((rope_len, 2), int)
    visited = {(0, 0)}
    with open("input.txt", "r") as f:
        for line in f:
            for _ in range(int(line.rstrip()[2:])):
                rope[0] += DIRECTIONS[line[0]]
                update_tail(rope)
                visited.add(tuple(rope[-1]))
    return visited


def main():
    print("P1:", len(simulate_rope(2)))
    print("P2:", len(simulate_rope(10)))


if __name__ == "__main__":
    main()
