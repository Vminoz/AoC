import numpy as np


def look_around(arr: np.ndarray, i: int, j: int):
    yield arr[i, :j][::-1]
    yield arr[:i, j][::-1]
    yield arr[i, j + 1 :]
    yield arr[i + 1 :, j]


def main():
    with open("input.txt") as f:
        forest = np.array([list(row.strip()) for row in f], int)
    visible = np.zeros_like(forest, bool)
    scenic = np.ones_like(forest, int)

    for pos, tree in np.ndenumerate(forest):
        for view in look_around(forest, *pos):
            next_higher = next(
                (i + 1 for i, o_tree in enumerate(view) if o_tree >= tree), 0
            )
            visible[pos] |= not next_higher
            scenic[pos] *= next_higher + (not next_higher) * len(view)

    print(visible.sum(), scenic.max())


if __name__ == "__main__":
    main()
