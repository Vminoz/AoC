LETTERSSTR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = {letter: i for i, letter in enumerate(LETTERSSTR, start=1)}


def check_comps(ruck):
    COMPS = 2
    split = len(ruck) // COMPS
    first = ruck[:split]
    second = ruck[split:]
    for letter in first:
        if letter in second:
            return LETTERS[letter]
    print("no common")
    return 0
    # next((LETTERS[letter] for letter in first if letter in second), 0)


def check_badges(group):
    shared = set(group[0])
    for row in group[1:]:
        shared_n = {letter for letter in shared if letter in row}
        shared = shared_n
    if len(shared) != 1:
        raise ValueError(f"Group {group} shares {shared}")
    return LETTERS[shared.pop()]


def main():
    prio1_sum = 0
    group = []
    prio2_sum = 0
    with open("input.txt", "r") as f:
        for lnr, line in enumerate(f):
            prio1_sum += check_comps(line[:-1])
            group.append(line[:-1])
            if lnr % 3 == 2:
                prio2_sum += check_badges(group)
                group = []

    print(prio1_sum)
    print(prio2_sum)


if __name__ == "__main__":
    main()
