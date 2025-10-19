import re

import numpy as np


def parse_sensors(file_name: str) -> dict:
    numbers = re.compile(r"-?\d+")
    sensors = {}
    with open(file_name) as f:
        for line in f:
            nums = [int(num) for num in numbers.findall(line)]
            sensors[(nums[0], nums[1])] = (nums[2], nums[3])
    return sensors


def scan_y(sensors: dict, y_coord: int, verb=False, xbnds=(-np.inf, np.inf)) -> set:
    coverage = set()
    for sensor, beacon in sensors.items():
        if verb:
            print("looking at sensor", sensor, end="\x1b[K\r")
        s_range = manhattan_2d(sensor, beacon)
        dy = abs(sensor[1] - y_coord)
        if dy > s_range:
            if verb:
                print("out of range", end="\x1b[K\r")
            continue
        probe_x(coverage, sensor[0], s_range - dy, xbnds)
    if xbnds[0] == -np.inf:
        coverage -= {b[0] for b in sensors.values() if b[1] == y_coord}
    if verb:
        print("\x1b[K", end="")
    return coverage


def probe_x(coverage: set, ox: int, dx: int, xbnds):
    run = 2
    xmi, xma = xbnds[0], xbnds[1]
    new_x = ox
    while run:
        if abs(new_x - ox) > dx or new_x > xma or new_x < xmi:
            run -= 1
            new_x = ox - 1
            continue
        if new_x not in coverage:
            coverage.add(new_x)
        new_x += 2 * run - 3


def covered_points(orig: tuple[int, int], man_dist: int) -> set[tuple[int, int]]:
    points = set()
    for i in range(man_dist + 1):
        for j in range(man_dist + 1 - i):
            for d in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                points.add((orig[0] + d[0] * i, orig[1] + d[1] * j))
    return points


def manhattan_2d(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def dark_coord(sensors: dict, lb=0, ub=4_000_000) -> tuple[int, int]:
    for y in range(lb, ub + 1):
        print("scanning", y, end=" ")
        scan = scan_y(sensors, y, False, (lb, ub))
        print("len:", len(scan), end="\x1b[K\r")
        # print(scan)
        if len(scan) < (ub - lb + 1):
            target = set(range(lb, ub + 1)) - scan
            if len(target) != 1:
                raise ValueError(f"position not unique, got {target}")
            print("\x1b[K", end="")
            return (target.pop(), y)
    raise ValueError(f"no free position found within [{lb},{ub}]")


def main():
    sensors = parse_sensors("input.txt")

    coverage = scan_y(sensors, 2_000_000, True)
    print(min(coverage), max(coverage))
    print("P1:", len(coverage))

    # Code below would take ~45 days to run
    lb, ub = 0, 4_000_000
    position = dark_coord(sensors, lb, ub)
    print(position)
    print("P2:", position[0] * 4_000_000 + position[1])


if __name__ == "__main__":
    main()
