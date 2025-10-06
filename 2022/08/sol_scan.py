import numpy as np

def scan(a:np.ndarray):
    visible_rows = np.zeros_like(a)
    c_max = -1
    for i,v in enumerate(a):
        if v > c_max:
            c_max = v
            visible_rows[i] = 1
    return visible_rows

def main():
    with open("in.txt") as f:
        forest = np.array([list(row.strip()) for row in f], int)
    forest = np.stack([forest, np.zeros_like(forest)])

    for _ in range(4):
        forest[1] |= np.apply_along_axis(scan, 1, forest[0].copy())
        forest = np.rot90(forest,1,(1,2))
    print(forest)
    print(forest[1].sum())

if __name__ == "__main__":
    main()