import math

SNAFU_NEG = {"=": -2, "-": -1, -1: "-", -2: "="}


def snafu_to_dec(snafu: str) -> int:
    return sum(
        int(SNAFU_NEG.get(ch, ch)) * 5**pow for pow, ch in enumerate(reversed(snafu))
    )


def dec_to_snafu(dec: int) -> str:
    digits = [0] * (int(math.log(dec, 5)) + 2)
    maxpow = len(digits)
    # Get coeffs
    for i, p in enumerate(reversed(range(maxpow))):
        if not i:
            continue
        quint_digit, dec = divmod(dec, 5**p)
        digits[i] = quint_digit
        j = i
        while quint_digit > 2:
            digits[j] -= 5
            digits[j - 1] += 1
            quint_digit = digits[j - 1]
            j -= 1
    if not digits[0]:
        digits.pop(0)  # ignore leading 0
    return "".join(SNAFU_NEG[d] if d < 0 else str(d) for d in digits)


def parse_fuel_reqs(file_name):
    with open(file_name) as f:
        snafu_reqs = f.read().splitlines()
    fuel_reqs = list(map(snafu_to_dec, snafu_reqs))
    return snafu_reqs, fuel_reqs


def main():
    fuel_requirements_dec = parse_fuel_reqs("input.txt")[1]
    p1_sol = dec_to_snafu(sum(fuel_requirements_dec))
    print("P1:", p1_sol)


if __name__ == "__main__":
    main()
