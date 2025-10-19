from collections import deque
from dataclasses import dataclass
from math import prod
from typing import Callable

OP_ALIAS = {"+": int.__add__, "*": int.__mul__}


@dataclass
class Monkey:
    items: deque
    divisor: int = 0
    partners: tuple[int, int] = (None, None)
    op: Callable = None
    inspect_cnt: int = 0
    worry_clip: int = 0

    def throw_to(self, monkeys: list, verbose=False):
        while self.items:
            self.inspect_cnt += 1
            item = self.items.pop()
            if verbose:
                print("Monke looks at item with WL:", item)
            item = self.op(item)
            if self.worry_clip:
                item %= self.worry_clip
            else:
                item //= 3
            target = self.partners[item % self.divisor > 0]
            monkeys[target].items.appendleft(item)
            if verbose:
                print(" → Item is now WL:", item)
            if verbose:
                print(" → Item thrown to", target)


def parse_input(file_name) -> list[Monkey]:
    monkey_list = []
    with open(file_name) as f:
        for line in f:
            if line[:3] != "  S":
                continue
            monkey = Monkey(
                deque(int(num) for num in reversed(line[18:-1].split(", ")))
            )
            line = next(f)
            operator = line[23]
            operand = line[25:-1]
            if operand == "old":
                monkey.op = lambda x, ot=operator: OP_ALIAS[ot](x, x)
            else:
                monkey.op = lambda x, ot=operator, on=int(operand): OP_ALIAS[ot](x, on)
            line = next(f)
            monkey.divisor = int(line[21:-1])
            line = next(f)
            partner_0 = int(line[-2])
            line = next(f)
            monkey.partners = (partner_0, int(line.rstrip()[-1]))
            monkey_list.append(monkey)
            print(monkey)
    return monkey_list


def do_round(monkeys, verbose=False):
    for i, m in enumerate(monkeys):
        if verbose:
            print("\nMonkey", i)
        m.throw_to(monkeys, verbose)


def show_hands(monkeys):
    print("\nMonke inventories:")
    for m in monkeys:
        print(str(m.items)[6:-1])


def main():
    monkeys = parse_input("input.txt")
    for i in range(20):
        do_round(monkeys, i == 0)
    show_hands(monkeys)
    monkeys = sorted(monkeys, key=lambda m: m.inspect_cnt)
    print("P1:", monkeys[-2].inspect_cnt * monkeys[-1].inspect_cnt)

    print("Now P2...")
    monkeys = parse_input("input.txt")
    giga_divisor = prod(m.divisor for m in monkeys)
    for m in monkeys:
        m.worry_clip = giga_divisor
    for i in range(10_000):
        if not i % 100:
            print(i, end="\r")
        do_round(monkeys)
    monkeys = sorted(monkeys, key=lambda m: m.inspect_cnt)
    print("P2:", monkeys[-2].inspect_cnt * monkeys[-1].inspect_cnt)


if __name__ == "__main__":
    main()
