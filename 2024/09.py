"""--- Day 9: Disk Fragmenter ---"""

from collections import deque
from typing import TypeAlias

from common import do_part, logger, parse_input_with
from common.ansi import HIGHLIGHT_END, HIGHLIGHT_START

FileSpec: TypeAlias = tuple[int, int, int]  # start_pos, id, size
DiskMap: TypeAlias = list[FileSpec]


def parse_disk_map(filename: str) -> DiskMap:
    with open(filename) as f:
        disk_map_str = f.read()

    fs = []
    position = 0
    for i, c in enumerate(disk_map_str):
        size = int(c)
        fs.append((position, -1 if i % 2 else i // 2, size))
        position += size
    if logger.is_verbose:
        logger.m(disk_map_repr(fs))
    return fs


def compact_fs_checksum(disk_map: DiskMap, fragment: bool = True) -> int:
    compact: DiskMap = []
    files = deque(c for c in disk_map if c[1] > -1)
    gaps = (c for c in disk_map if c[1] == -1)

    while files:
        pos, _, size = next(gaps)
        while files and files[0][0] < pos:
            # Take those that won't move
            compact.append(files.popleft())

        if fragment:  # Fill blockwise from right
            blocks = block_compact(files, size, pos)
        else:  # Fill filewise from right
            blocks = file_compact(files, size, pos)
        compact.extend(blocks)

        if logger.is_debug:
            logger.v("gap:", pos, size, "blocks:", blocks)
            logger.v(files)
            logger.m(disk_map_repr(compact, list(files)))

    if logger.is_verbose:
        logger.m(disk_map_repr(compact))

    return calc_checksum(compact)


def block_compact(fs: deque[FileSpec], free: int, position: int) -> DiskMap:
    blocks = []
    while free and fs:
        pos, file_id, size = fs.pop()
        if size > free:
            blocks.append((position, file_id, free))
            fs.append((pos, file_id, size - free))
            position += free
            free = 0
        else:
            blocks.append((position, file_id, size))
            free -= size
            position += size
    return blocks


def file_compact(fs: deque[FileSpec], free: int, position: int) -> DiskMap:
    blocks = []
    restore = []
    while free and fs:
        pos, file_id, size = fs.pop()
        if size <= free:
            blocks.append((position, file_id, size))
            free -= size
            position += size
        else:
            restore.append((pos, file_id, size))
    fs.extend(reversed(restore))
    return blocks


def calc_checksum(fs: DiskMap) -> int:
    """
    sum(id * block_index) for all blocks of each id
    """
    chsm = 0
    for pos, file_id, size in fs:
        block_pos = pos
        for _ in range(size):
            chsm += file_id * block_pos
            block_pos += 1
    return chsm


def disk_map_repr(dm: DiskMap, alt: DiskMap | None = None) -> str:
    alt = alt or []
    max_p = dm[-1][0] if dm else 0
    highligted = False
    s = ""
    position = 0
    for pos, file_id, size in dm + alt:
        if pos > max_p:
            s += HIGHLIGHT_START
        s += "·" * (pos - position)
        s += str("." if file_id == -1 else file_id) * size
        position = pos + size
    if highligted:
        s += HIGHLIGHT_END
    return s


def main():
    do_part(1, compact_fs_checksum, parse_input_with(parse_disk_map))
    do_part(2, compact_fs_checksum, parse_input_with(parse_disk_map), fragment=False)


if __name__ == "__main__":
    main()
