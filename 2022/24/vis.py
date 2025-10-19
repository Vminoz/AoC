import pickle as pkl
from pathlib import Path

import matplotlib as mpl
import numpy as np
from matplotlib import animation as ma
from matplotlib import colors as mc
from matplotlib import pyplot as plt
from sol import Valley, valley_a_star


def animate_path(
    valley: Valley,
    path: list[tuple[int, int]],
    visited: list[set[tuple[int, int]]],
    gif=False,
):
    "Animate a game and save as a GIF"
    p = list(zip(*path))

    fdpi = 10 / plt.rcParams["figure.dpi"]
    h, w = valley.field.shape
    fig = plt.figure(figsize=(fdpi * w, fdpi * h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    greenish = np.array([0.75, 1, 0.66, 1])
    bincmap = mpl.colormaps["binary"].resampled(6)(np.linspace(0, 1, 6))
    bincmap[0] = greenish
    colmap = mc.ListedColormap(bincmap)

    im = ax.imshow(valley.field, cmap=colmap)
    scat = ax.scatter(x=p[1][0], y=p[0][0], c="r", s=40, zorder=100, marker="s")
    visit_scat = ax.scatter(x=p[1][0], y=p[0][0], c="g", s=40, zorder=80, marker="s")
    (line,) = ax.plot(p[1][:1], p[0][:1], c="r", linewidth=2, zorder=80)
    patches = [line, scat, visit_scat, im]
    new_cols = iter(("m", "r", "m"))
    t0 = 0

    def animation_update(t):
        """anim update function"""
        nonlocal t0
        if t:
            valley.step_field()
        if t and t - t0 > 100 and path[t] in (valley.start, valley.end):
            character_col = next(new_cols)
            print("at", t, "new color", character_col)
            line.set_color(character_col)
            scat.set_color(character_col)
            t0 = t
        im.set_data(valley.field)
        line.set_data(p[1][t0 : t + 1], p[0][t0 : t + 1])
        scat.set_offsets((p[1][t], p[0][t]))
        visit_scat.set_offsets(list(map(lambda x: (x[1], x[0]), visited[t])))
        return patches

    anim = ma.FuncAnimation(fig, animation_update, frames=len(path), blit=True)
    if gif:
        writergif = ma.PillowWriter(fps=5)
        anim.save("24.gif", writer=writergif)
    else:
        writermp4 = ma.FFMpegWriter(fps=5)
        anim.save("24.mp4", writer=writermp4)
    plt.clf()
    print("Saved video")


def main():
    to_read = "input.txt"
    pickle_file = "pickles/path_" + to_read.replace(".", "") + ".pkl"
    if Path(pickle_file).is_file():
        with open(pickle_file, "rb") as f:
            (path, visited) = pkl.load(f)
    else:
        valley = Valley.from_file(to_read)
        res = valley_a_star(valley, True)
        path = res[1][::-1]
        visited = res[2]
        with open(pickle_file, "wb+") as f:
            pkl.dump((path, visited), f)
    for gif in (True, False):
        valley = Valley.from_file(to_read)
        animate_path(valley, path, visited, gif)


if __name__ == "__main__":
    main()
