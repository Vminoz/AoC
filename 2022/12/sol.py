import numpy as np
from vis import MountainMap, fail_plot

IGNORE = 1_000_000


def neighbors2d(index, shape):
    neighbors = index + np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    valid = (
        (neighbors[:, 0] >= 0)
        & (neighbors[:, 0] < shape[0])
        & (neighbors[:, 1] >= 0)
        & (neighbors[:, 1] < shape[1])
    )
    return (bi(neighbor) for neighbor in neighbors[valid])


def bi(x) -> tuple:
    return x[0], x[1]


def pathfinder(mountain: np.ndarray, start, end, animate=False, do_fail_plot=False):
    mshape = mountain.shape
    dist = np.ones(mshape) * np.inf
    dist[start] = 0
    visited = np.zeros(mshape, bool)
    bias = np.array(
        [
            [
                IGNORE * (1 - ((i, j) == start)) + (abs(end[0] - i) + abs(end[1] - j))
                for j in range(mshape[1])
            ]
            for i in range(mshape[0])
        ]
    )
    prev = {index: (None, None) for index in np.ndindex(mshape)}

    m_map = MountainMap(mountain, start, end) if animate else None
    while (bias < IGNORE).any():
        u = np.unravel_index((dist + bias).argmin(), mshape)
        if u == end:
            if animate:
                m_map.flip_pov()
            path = backtrack(u, start, prev)
            if animate:
                m_map.show_path(path)
            return True, path
        bias[u] += IGNORE
        visited[u] = True
        nbs, nbs_c = update_neighbors(mountain, mshape, dist, bias, prev, u)

        if animate:
            m_map.update(visited, nbs, nbs_c)

    if animate:
        m_map.update(visited, [], [])
    if do_fail_plot:
        fail_plot(dist, bias)
    return False, np.argwhere(visited)


def update_neighbors(mountain, mshape, dist, bias, prev, u):
    nbs = []
    nbs_c = []
    for v in neighbors2d(u, mshape):
        nbs.append(v[::-1])
        nbs_c.append("r")
        if mountain[v] > mountain[u] + 1:
            continue
        alt = dist[u] + 1
        if alt < dist[v]:
            dist[v] = alt
            prev[v] = u
            if bias[v] >= IGNORE:
                bias[v] -= IGNORE
            nbs_c[-1] = "b"
    return nbs, nbs_c


def backtrack(u, start, prev):
    path = []
    while u != start:
        u = prev[u]
        path.append(u[::-1])
    return path


def parse_input(file_name: str) -> np.ndarray:
    with open(file_name) as f:
        mountain = [[ord(lett) - 97 for lett in line.rstrip()] for line in f]
    mountain = np.array(mountain)
    s = bi(np.argwhere(mountain == -14)[0])
    mountain[s] = 0
    e = bi(np.argwhere(mountain == -28)[0])
    mountain[e] = 25
    return mountain, s, e


def main():
    mountain, S, E = parse_input("input.txt")

    p1_path = pathfinder(mountain, S, E, True)[1]
    p1_sol = len(p1_path)
    print("P1:", p1_sol)

    MountainMap.map_counter += 2
    best = (None, None, np.inf)
    prospects = {bi(index) for index in np.argwhere(mountain == 0)}
    while prospects:
        if not (MountainMap.map_counter - 1) % 10:
            print(MountainMap.map_counter, end="\r")
        s = bi(prospects.pop())
        success, res = pathfinder(mountain, s, E, True)
        if success:
            alt = len(res)
            if alt < best[2]:
                best = (s, res, alt)
                MountainMap.ref_path = res
        else:
            for visited_index in res:
                prospects.discard(bi(visited_index))
    m_map = MountainMap(mountain, best[0], E)
    m_map.show_path(best[1][:-1], "y")
    print("P2:", best[2])


if __name__ == "__main__":
    main()
