"""--- Day 2: Red-Nosed Reports ---"""

from common import do_part_on_input, lines, logger


def count_safe_reports(filename: str, dampen: bool = False):
    safe = 0
    for line in lines(filename):
        nums = [int(i) for i in line.rstrip().split()]
        logger.d(nums)
        safe += is_safe(nums, dampen)
    return safe


def is_safe(nums: list[int], dampen: bool = False) -> bool:
    def fail(at: int) -> bool:
        if dampen:
            logger.v(f"❌ {at}")
            # edge case
            if (at == 2) and is_safe(nums[1:]):
                return True
            # excl current
            popped = nums.pop(at)
            if is_safe(nums):
                return True
            # excl previous
            nums[at - 1] = popped
            return is_safe(nums)
        return False

    is_decreasing = None
    for i, num in enumerate(nums[1:], start=1):
        prev = nums[i - 1]
        step = num - prev
        step_is_neg = step < 0

        # direction
        if is_decreasing is None:
            is_decreasing = step_is_neg
        elif is_decreasing != step_is_neg:
            logger.v(
                f"❗should {'decrease' if is_decreasing else 'increase'} at\t{i}:{prev}→{num}\t{nums}"
            )
            return fail(i)

        # step size
        if not (0 < abs(step) < 4):
            logger.v(f"❗bad step {step: >3} at\t{i}:{prev}→{num}\t{nums}")
            return fail(i)
    if not dampen:
        logger.v(f"✅{nums}")
    return True


def main():
    do_part_on_input(1, count_safe_reports)
    do_part_on_input(2, count_safe_reports, dampen=True)


if __name__ == "__main__":
    main()
