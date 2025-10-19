from collections import Counter

from common import do_part_on_input, lines, logger

TYPE_STRENGTH = {t: i for i, t in enumerate(["h", "2", "p", "3", "f", "4", "5"])}
CARD_STRENGTH = {c: i for i, c in enumerate("23456789TJQKA")}


class Hand:
    def __init__(self, cards: str, bid: int, joker: bool = False):
        self.cards = cards
        card_strength = CARD_STRENGTH
        self.jokers = False
        if joker and "J" in cards:
            card_strength["J"] = -1
            self.jokers = True
        self.type = self._get_type()
        self.s_c = [card_strength[c] for c in cards]
        self.bid = bid
        self.s_t = TYPE_STRENGTH[self.type]

    def _get_type(self) -> str:
        card_count = Counter(self.cards)
        jokers = card_count.pop("J", 0)
        highest_cnt = max(card_count.values()) if card_count else 0
        highest_cnt += jokers
        logger.v(card_count, highest_cnt)
        if highest_cnt in (5, 4):
            return str(highest_cnt)
        if len(card_count) == 2:
            return "f"
        if highest_cnt == 3:
            return "3"
        if len(card_count) == 3:
            return "p"
        if highest_cnt == 2:
            return "2"
        return "h"

    def __lt__(self, other: "Hand") -> bool:
        if self.s_t != other.s_t:
            return self.s_t < other.s_t
        for c, oc in zip(self.s_c, other.s_c):
            if c != oc:
                return c < oc
        raise ValueError("idk", self, other)

    def __repr__(self) -> str:
        return f"h:{self.cards}({(self.s_c)}), b:{self.bid}, t:{self.type}({self.s_t})"


def winnings(filename: str, joker: bool = False):
    hands = [Hand(h, int(b), joker) for h, b in map(str.split, lines(filename))]
    hands_sorted = sorted(hands)
    if logger.level == 2:
        logger.v("\n".join(map(str, hands)))
        logger.v(*(h.cards for h in hands_sorted))
    return sum(i * h.bid for i, h in enumerate(hands_sorted, 1))


def main():
    do_part_on_input(1, winnings)
    do_part_on_input(2, winnings, joker=True)


if __name__ == "__main__":
    main()
