from pathlib import Path
from common import logger, P3D, do_part_on_input
from typing import TypeAlias
from collections import defaultdict as DD, deque as DQ, Counter as CT

Brick: TypeAlias = tuple[P3D, ...]
BrickTower: TypeAlias = DD[Brick, tuple[set[Brick], set[Brick]]]


def read_bricks(filename) -> list[Brick]:
    bricks = []
    for line in open(filename).read().split("\n"):
        start, end = (
            tuple(map(int, part.split(","))) for part in line.rstrip().split("~")
        )

        if start == end:
            bricks.append((start,))
            continue

        for i, se in enumerate(zip(start, end)):
            s, e = se
            if s != e:
                break
        else:
            raise ValueError(f"didn't find length axis from {start}, {end}")
        extrude = e - s
        assert extrude > 0, f"{start} {end} {s} {e}"
        block = list(start)
        brick = [start]
        for _ in range(extrude):
            block[i] += 1
            brick.append(tuple(block))
        bricks.append(tuple(brick))
    return bricks


def lowest_block_z(brick: Brick) -> int:
    return min(block[2] for block in brick)


def drop_brick(brick: Brick) -> Brick:
    return tuple(drop(block) for block in brick)


def drop(pos: P3D) -> P3D:
    return pos[:2] + (pos[2] - 1,)


def drop_hard(brick: Brick, blocks: dict[P3D, Brick]) -> tuple[Brick, set[Brick]]:
    supports = set()
    while not supports:
        next_brick = drop_brick(brick)
        for block in next_brick:
            if block[2] == 0:
                return brick, set()
            if block in blocks:
                supports.add(blocks[block])
        if not supports:
            brick = next_brick
    return brick, supports


def drop_all(falling_bricks: list[Brick]) -> BrickTower:
    falling_bricks.sort(key=lowest_block_z, reverse=True)
    logger.d(f"→ Falling:\n{falling_bricks}")

    brick_sequence = []
    block_to_brick: dict[P3D, Brick] = {}
    tower: BrickTower = DD(lambda: (set(), set()))
    while falling_bricks:
        brick = falling_bricks.pop()
        logger.d("↓", brick)

        brick, supports = drop_hard(brick, block_to_brick)
        logger.d("─", brick)
        for block in brick:
            block_to_brick[block] = brick

        tower[brick][0].update(supports)
        for s in supports:
            tower[s][1].add(brick)

        if logger.is_verbose:
            brick_sequence.append([*tower, *falling_bricks])

    if logger.is_verbose:
        with open(Path(__file__).parent / "vis" / "--22.txt", "w") as f:
            for state in brick_sequence:
                print(state, file=f)
    return tower


def count_removable(tower: BrickTower) -> int:
    support_count = {b: len(tower[b][0]) for b in tower}
    cnt = 0
    for brick in tower:
        if all(support_count[s] > 1 for s in tower[brick][1]):
            cnt += 1
    return cnt


def sum_chain_reaction(tower: BrickTower) -> int:
    """For each brick, determine how many other bricks would fall if that brick
    was removed (all uniquely above).
    What is the sum of the number of other bricks that would fall?
    """
    bricks = list(tower.keys())
    bricks.sort(key=lowest_block_z, reverse=True)
    support_count = CT({b: len(tower[b][0]) for b in tower})
    memo = {}
    result = 0
    for brick in bricks:
        logger.v("p", brick)
        result += count_toppled(tower, support_count, memo, brick)
    logger.d("\n".join(f"{b} {f} {p}\n" for b, (f, p) in memo.items()))
    return result


def count_toppled(
    tower: BrickTower,
    support_count: CT[Brick],
    memo: dict[Brick, tuple[int, CT[Brick]]],
    brick: Brick,
) -> int:
    full_rm = 0
    supports_removed = CT()
    falling_dq = DQ()
    for c in tower[brick][1]:
        supports_removed[c] += 1
        if supports_removed[c] == support_count[c]:
            supports_removed.pop(c)
            falling_dq.append(c)

    while falling_dq:
        child_brick = falling_dq.popleft()

        logger.d("c", child_brick)
        full_rm += 1

        logger.d("m")
        cf, cp = memo[child_brick]
        full_rm += cf
        supports_removed += cp

        for c in list(supports_removed.keys()):
            if supports_removed[c] == support_count[c]:
                supports_removed.pop(c)
                falling_dq.append(c)

    memo[brick] = (full_rm, supports_removed)
    logger.d("r", full_rm)
    return full_rm


def part1(filename: str):
    falling_bricks = read_bricks(filename)
    logger.d(falling_bricks)
    cnt = count_removable(drop_all(falling_bricks))
    return cnt


def part2(filename: str):
    falling_bricks = read_bricks(filename)
    tower = drop_all(falling_bricks)
    return sum_chain_reaction(tower)


def main():
    do_part_on_input(1, part1)
    do_part_on_input(2, part2)


if __name__ == "__main__":
    main()
