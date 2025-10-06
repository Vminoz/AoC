from common import do_part, lines, logger, parse_input_with

TURNS = {
    "F": (1, 1),
    "J": (-1, -1),
    "L": (-1, 1),
    "7": (1, -1),
}

PIPES = {
    "-": "─",
    "|": "│",
    "F": "┌",
    "J": "┘",
    "L": "└",
    "7": "┐",
}

PTURNS = {
    "┌": (1, 1),
    "┘": (-1, -1),
    "└": (-1, 1),
    "┐": (1, -1),
}


def read_maze(filename: str) -> list[list[str]]:
    return [list(line.strip()) for line in lines(filename)]


def loop_steps(maze: list[list[str]]):
    i, j, di, dj = first_step(maze)
    si, sj = di, dj
    steps = 1
    here = maze[i][j]
    while here != "S":
        maze[i][j] = PIPES[here]
        if here in TURNS:
            if di:  # moving vertically
                di = 0
                dj = TURNS[here][1]
            else:  # moving horizontally
                dj = 0
                di = TURNS[here][0]
        steps += 1
        i, j = i + di, j + dj
        here = maze[i][j]
    # get angle of S
    maze[i][j] = PIPES[get_pipe(max(si, -di, key=abs), max(sj, -dj, key=abs))]
    show_maze(maze)
    return steps // 2


def get_pipe(i: int, j: int) -> str:
    for ch, outlets in TURNS.items():
        if outlets == (i, j):
            return ch
    raise ValueError("Could not find pipe")


def show_maze(maze):
    if logger.level > 1:
        logger.m("\n".join("".join(row) for row in maze))


def first_step(maze: list[list[str]]) -> tuple[int, int, int, int]:
    for i, row in enumerate(maze):
        if "S" in row:
            j = row.index("S")
            return valid_step(maze, i, j)
    raise ValueError("Could not find start")


def valid_step(maze: list[list[str]], i: int, j: int) -> tuple[int, int, int, int]:
    i_range = range(len(maze))
    j_range = range(len(maze[0]))
    if i + 1 in i_range and maze[i + 1][j] in "|LJ":
        return i + 1, j, 1, 0
    if i - 1 in i_range and maze[i - 1][j] in "|F7":
        return i + 1, j, -1, 0
    if j + 1 in j_range and maze[i][j + 1] in "-7J":
        return i, j + 1, 0, 1
    if j - 1 in i_range and maze[i][j - 1] in "-LF":
        return i, j - 1, 0, -1
    raise ValueError("No valid step")


def count_contained(maze: list[list[str]]) -> int:
    cnt = 0
    for i, row in enumerate(maze):
        inside = False
        pipe_i = 0
        for j, cell in enumerate(row):
            if cell == "─":
                continue
            if cell == "│":
                inside = not inside
            elif cell in PTURNS:
                if not pipe_i:
                    pipe_i = PTURNS[cell][0]
                else:
                    if PTURNS[cell][0] != pipe_i:  # s shape
                        inside = not inside
                    pipe_i = 0
            elif inside and cell not in PTURNS:
                cnt += 1
                maze[i][j] = "【█】"
    show_maze(maze)
    return cnt


def main():
    maze = parse_input_with(read_maze)
    do_part(1, loop_steps, maze)
    do_part(2, count_contained, maze)


if __name__ == "__main__":
    main()
