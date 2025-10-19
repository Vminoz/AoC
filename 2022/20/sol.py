def mix(nums: list, order: list, n: int):
    for i in range(n):
        idx = order.index(i)
        order.pop(idx)
        num = nums.pop(idx)
        new_i = (idx + num) % (n - 1)
        order.insert(new_i, i)
        nums.insert(new_i, num)


def decrypt(nums: list, n: int):
    for i in range(n):
        if nums[i] == 0:
            return sum(nums[(i + j) % n] for j in [1000, 2000, 3000])


def main():
    file_name = "input.txt"
    with open(file_name) as f:
        orig_nums = [int(num) for num in f.readlines()]
    N = len(orig_nums)

    nums = orig_nums[:]
    order = list(range(N))
    mix(nums, order, N)
    print("P1:", decrypt(nums, N))

    nums = [num * 811589153 for num in orig_nums]
    order = list(range(N))
    for _ in range(10):
        mix(nums, order, N)
    print("P2:", decrypt(nums, N))


if __name__ == "__main__":
    main()
