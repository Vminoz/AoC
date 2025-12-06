# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib==3.10",
#     "numpy==2.3",
#     "tqdm==4.67",
# ]
# ///
import ast
from typing import TypeAlias

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

StaticBrick: TypeAlias = tuple[tuple[int, int, int], ...]


def parse_brick_sequence(filename: str, step: int = 100) -> list[list[StaticBrick]]:
    seq = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i % step:
                continue
            seq.append(ast.literal_eval(line))
    seq.append(ast.literal_eval(line))  # ensure the last line
    return seq


def animate_bricks(
    brick_sequence: list[list[StaticBrick]],
    filename: str = "",
    line_plots=False,
):
    plt.rcParams["savefig.transparent"] = True
    plt.rcParams["savefig.pad_inches"] = 0

    # squate figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")
    ax.view_init(10, 45)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1.5), zoom=1.66)

    padding = 5
    max_x = (
        max(np.array(brick)[:, 0].max() for brick in brick_sequence[0]) + 2 * padding
    )
    max_y = (
        max(np.array(brick)[:, 1].max() for brick in brick_sequence[0]) + 2 * padding
    )
    max_z = max(np.array(brick)[:, 2].max() for brick in brick_sequence[0]) + padding

    def max_all_axes(length: int):
        ax.set_xlim(0, length)
        ax.set_ylim(0, length)
        ax.set_zlim(0, length * 1.5)

    max_all_axes(max_z)

    if line_plots:
        X, Y = np.meshgrid([-padding, max_x], [-padding, max_y])
        Z = np.zeros_like(X)
        ax.plot_surface(X, Y, Z, color="g", alpha=1, zorder=1)
        path_list = []
        for brick in brick_sequence[0]:
            brick = list(zip(*brick))
            (path,) = ax.plot(*brick, marker="o", linestyle="-", color="r", zorder=10)
            path_list.append(path)

        def update(frame):
            for path, brick in zip(path_list, brick_sequence[frame]):
                brick = list(zip(*brick))
                path.set_data(brick[0], brick[1])
                path.set_3d_properties(brick[2])
                ax.dist = frame + 1

    else:
        x, y, z = np.indices((max_x, max_y, max_z))
        ground = z == 0
        colors = np.empty(ground.shape, dtype=object)
        e_colors = np.empty(ground.shape, dtype=object)
        colors[ground] = "gray"

        def update(frame):
            # remove previous voxels
            for thing in ax.collections:
                thing.remove()
            colors[~ground] = None
            e_colors[~ground] = None
            voxelarray = ground.copy()
            zmax = 0
            for brick in brick_sequence[frame]:
                for block in brick:
                    block = np.array(block) + np.array([padding, padding, 0])
                    voxelarray |= (x == block[0]) & (y == block[1]) & (z == block[2])
                    if block[2] > zmax:
                        zmax = block[2]
            # render the voxels in front of the ground surface
            colors[voxelarray & ~ground] = "red"
            e_colors[voxelarray & ~ground] = "black"
            ax.voxels(voxelarray, facecolors=colors)

            max_all_axes(zmax)

    anim = FuncAnimation(
        fig,
        update,
        frames=tqdm(range(len(brick_sequence))),
        repeat=True,
    )

    anim.save(filename, fps=30, dpi=1200, extra_args=["-vcodec", "libx264"])


def main():
    from sys import argv

    if len(argv) < 2:
        print(
            f"Usage: {argv[0]} <sequence_file> [filename=anim.mp4] [step=100]",
            "Note: create a sequence file with 2023.22 -v",
            sep="\n",
        )
        return
    animate_bricks(
        parse_brick_sequence(
            argv[1],
            step=int(argv[3]) if len(argv) > 3 else 100,
        ),
        argv[2] if len(argv) > 2 else "anim.mp4",
    )


if __name__ == "__main__":
    main()
