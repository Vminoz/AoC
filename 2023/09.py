from common import argv_input_file, lines, logger, do_part_on_input


def bootleg_tsa(filename: str, inplace=True, neg: bool = False):
    res = 0
    for line in lines(filename):
        nums = [int(num) for num in line.split()]
        logger.v(nums)
        if neg:
            nums.reverse()

        while not all(n == 0 for n in nums):
            res += nums[-1]
            if inplace:
                inplace_diff(nums)
            else:
                nums = diff(nums)
            logger.v(nums)

    return res


def inplace_diff(arr: list) -> None:
    prev = arr[0]
    for i, n in enumerate(arr[1:]):
        arr[i] = n - prev
        prev = n
    arr.pop()  # rm last


def diff(arr: list) -> list:
    return [arr[i + 1] - n for i, n in enumerate(arr[:-1])]


def main():
    from sys import argv

    if "-b" in argv:
        logger.m("【False】 list comp every diff operation, 【True】 mutates the lists")
        for inplace in (True, False):
            logger.bench(bootleg_tsa, argv_input_file(), inplace=inplace)
    do_part_on_input(1, bootleg_tsa)
    do_part_on_input(2, bootleg_tsa, neg=True)


if __name__ == "__main__":
    main()
