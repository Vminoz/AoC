"""--- Day 6: Guard Gallivant ---"""

from typing import TypeAlias

from common import P2D, do_part, lines, logger, parse_input_with
from common.maths import BBox
from common.visuals import p2d_sets_string

CLOCKWISE: dict[P2D, P2D] = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}
ARROW = {
    (-1, 0): "↑",
    (0, 1): "→",
    (1, 0): "↓",
    (0, -1): "←",
}
MAX_STEPS = 100_000


GuardState: TypeAlias = tuple[P2D, P2D]  # position, direction
CheckResult: TypeAlias = set[GuardState] | None
Shortcuts: TypeAlias = dict[
    GuardState, tuple[GuardState | None, set[P2D]]
]  # state, (next_state, states)


def parse_map(filename: str) -> tuple[P2D, set[P2D]]:
    guard_pos = None
    obstacles: set[P2D] = set()
    for i, line in enumerate(lines(filename)):
        for j, c in enumerate(line):
            if c == ".":
                continue
            if c == "#":
                obstacles.add((i, j))
            elif c == "^":
                guard_pos = (i, j)
    if guard_pos is None:
        raise ValueError("no guard?")
    return guard_pos, obstacles


def step(
    state: GuardState,
    obstacles: set[P2D],
    bbox: BBox,
) -> GuardState | None:
    """Returns None if guard is out of bounds"""
    p, d = state
    np = (p[0] + d[0], p[1] + d[1])
    if np in obstacles:
        return (p, CLOCKWISE[d])
    if np not in bbox:
        return None
    return (np, d)


def step_until_turn(
    state: GuardState,
    obstacles: set[P2D],
    bbox: BBox,
    include_obstacle: bool = False,
) -> tuple[GuardState | None, set[P2D]]:
    visited: set[P2D] = set()
    while True:
        visited.add(state[0])
        new_state = step(state, obstacles, bbox)
        if new_state is None:
            return None, visited
        if new_state[1] != state[1]:
            if include_obstacle:
                # add obstacle hit
                visited.add((state[0][0] + state[1][0], state[0][1] + state[1][1]))
            return new_state, visited
        state = new_state


def count_guard_visited(guard_pos: P2D, obstacles: set[P2D]) -> int:
    state: GuardState = (guard_pos, (-1, 0))  # Up
    visited: set[P2D] = set()
    bbox = BBox.from_tuples(obstacles)
    for _ in range(MAX_STEPS):
        new_state, v = step_until_turn(state, obstacles, bbox)
        visited |= v
        if logger.is_verbose:
            logger.m("\n" + p2d_sets_string(visited, obstacles))
        if new_state is None:
            return len(visited)
        state = new_state
    raise RuntimeError("Took 1M steps, something is wrong")


def count_looping_obstacles(guard_pos: P2D, obstacles: set[P2D]) -> int:
    """
    until exiting:
        step
        if front pos not visited:
            place obstacle
            while inside:
                step
                if revisiting pos,dir pair:
                    cnt += 1
                    break
            pop obstacle
    """
    state: GuardState = (guard_pos, (-1, 0))  # Up
    visited: set[P2D] = set()
    bbox = BBox.from_tuples(obstacles)
    count = 0
    warp: Shortcuts = {}
    for _ in range(MAX_STEPS):
        new_state = step(state, obstacles, bbox)
        if new_state is None:
            return count

        pos = new_state[0]
        if pos not in visited:
            try_obstacle = pos
            if try_obstacle not in obstacles and try_obstacle in bbox:
                obstacles.add(try_obstacle)
                states = check_if_looping(
                    state,
                    obstacles,
                    bbox,
                    warp,
                    try_obstacle,
                )
                if logger.is_verbose and states is not None:
                    show_states(states, obstacles, try_obstacle, visited, warp)
                count += states is not None
                obstacles.remove(try_obstacle)
            else:
                logger.v(
                    "not trying",
                    try_obstacle,
                    try_obstacle not in obstacles,
                    try_obstacle in bbox,
                )

        state = new_state
        visited.add(pos)
    raise RuntimeError("Took many steps, something is wrong")


def show_states(
    states: set[GuardState],
    obstacles: set[P2D],
    mark: P2D,
    visited: set[P2D],
    warp: Shortcuts,
):
    logger.m(
        "\n"
        + p2d_sets_string(
            {s[0] for s in states},
            obstacles,
            symbols={mark: "X"},
            secondary_symbols={
                **{_: "░" for _ in visited},
                **{p: ARROW[d] for p, d in warp},
            },
        )
    )


def check_if_looping(
    state: GuardState,
    obstacles: set[P2D],
    bbox: BBox,
    warp: Shortcuts,
    new_obstacle: P2D,
) -> CheckResult:
    """Only returns the state set for visualisation, could be bool"""
    states: set[GuardState] = set()
    visited: set[P2D] = set()
    new_state: GuardState | None = None
    skip_cache = True
    for _ in range(MAX_STEPS):
        warped = False
        if state in warp:
            new_state, visited = warp[state]
            if new_obstacle not in visited:
                warped = True

        if not warped:
            new_state, visited = step_until_turn(
                state, obstacles, bbox, include_obstacle=True
            )
            if not skip_cache and new_obstacle not in visited:
                warp[state] = (new_state, visited)

            skip_cache = new_obstacle in visited

        if logger.is_debug:
            show_states(states, obstacles, new_obstacle, visited, warp)

        if new_state is None:
            return None
        state = new_state
        if state in states:
            return states
        states.add(state)

    raise RuntimeError("Took many steps, something is wrong")


def main():
    guard_pos, obstacles = parse_input_with(parse_map)
    do_part(1, count_guard_visited, guard_pos, obstacles)
    do_part(2, count_looping_obstacles, guard_pos, obstacles)


if __name__ == "__main__":
    main()
