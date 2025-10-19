import numpy as np
from matplotlib import pyplot as plt


def fail_plot(dist, bias):
    _, ax = plt.subplots(2, 1)
    ax[0].imshow(bias)
    ax[1].imshow(dist)
    plt.axis("off")
    plt.show()


class MountainMap:
    map_counter = -1
    ref_path = []

    def __init__(self, mountain: np.ndarray, start: tuple, goal: tuple) -> None:
        MountainMap.map_counter += 1
        self.start = start[::-1]
        self.goal = goal[::-1]
        fdpi = 10 / plt.rcParams["figure.dpi"]
        h, w = mountain.shape
        self.fig = plt.figure(figsize=(fdpi * w, fdpi * h))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.axis("off")
        self.ax.imshow(mountain, cmap="pink")
        self.ax.scatter(
            (start[1], goal[1]), (start[0], goal[0]), c=("y", "k"), marker="*"
        )
        self.sca_vis = self.ax.scatter(start[1], start[0], c="g", s=2, marker="s")
        self.sca_pov = self.ax.scatter(start[1], start[0], c="r", s=20, marker="s")
        self.frame_num = 0

    def update(self, visited, nbs, nbs_c):
        if MountainMap.map_counter and nbs:
            return
        where_visited = np.argwhere(visited)[:, ::-1]
        if not nbs:
            self._show_ref()
            self._update_pov(where_visited, "r")
            plt.close()
            return
        self.sca_vis.set_offsets(where_visited)
        self._update_pov(nbs, nbs_c)

    def _update_pov(self, offs, cols):
        self.sca_pov.set_offsets(offs)
        self.sca_pov.set_color(cols)
        self.make_frame()

    def _show_ref(self):
        if MountainMap.ref_path:
            self.sca_vis.set_offsets(MountainMap.ref_path)
            self.sca_vis.set_color("y")

    def flip_pov(self):
        self.sca_pov.set_offsets([self.goal])
        self.sca_pov.set_color("b")
        self.sca_vis.set_color((0, 0, 0, 0.5))

    def show_path(self, path, c=None):
        if c is not None:
            self.sca_pov.set_color(c)
        if MountainMap.map_counter:
            self._show_ref()
            self.sca_pov.set_offsets(path)
            self.make_frame()
        else:
            for i, _ in enumerate(path[:-1], start=1):
                self.sca_pov.set_offsets(path[:i])
                self.make_frame()
        plt.close()

    def make_frame(self):
        self.frame_num += 1
        if MountainMap.map_counter:
            file_name = f"frames/2/{MountainMap.map_counter:04}.png"
        else:
            if not self.frame_num % 100:
                print(self.frame_num, end="\r")
            file_name = f"frames/1/{self.frame_num:04}.png"

        self.fig.savefig(file_name)
