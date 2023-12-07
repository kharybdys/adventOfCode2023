from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar, Self, Counter


class HandType(IntEnum):
    SINGLE_CARD = 0
    PAIR = 1
    DOUBLE_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


@dataclass(order=True)
class Hand:
    hand_type: HandType
    cards: str
    bid: int

    T_chr: ClassVar[str] = chr(ord("9") + 1)
    J_chr: ClassVar[str] = chr(ord("9") + 2)
    Q_chr: ClassVar[str] = chr(ord("9") + 3)
    K_chr: ClassVar[str] = chr(ord("9") + 4)
    A_chr: ClassVar[str] = chr(ord("9") + 5)

    def __repr__(self):
        orig_cards = self.cards.replace(self.A_chr, "A").replace(self.K_chr, "K").replace(self.Q_chr, "Q").replace(self.J_chr, "J").replace(self.T_chr, "T")
        return f"Hand[type={self.hand_type}, cards={orig_cards}, bid={self.bid}]"

    @staticmethod
    def from_string(line: str) -> Self:
        orig_cards, bid_str = line.split()
        cards_count = Counter(orig_cards)
        print(f"{cards_count=}, {line=}, {list(sorted(cards_count.values()))=}")
        if 5 in cards_count.values():
            hand_type = HandType.FIVE_OF_A_KIND
        elif 4 in cards_count.values():
            hand_type = HandType.FOUR_OF_A_KIND
        elif 3 in cards_count.values() and 2 in cards_count.values():
            hand_type = HandType.FULL_HOUSE
        elif 3 in cards_count.values():
            hand_type = HandType.THREE_OF_A_KIND
        elif [1, 2, 2] == list(sorted(cards_count.values())):
            hand_type = HandType.DOUBLE_PAIR
        elif 2 in cards_count.values():
            hand_type = HandType.PAIR
        else:
            hand_type = HandType.SINGLE_CARD
        cards = orig_cards.replace("T", Hand.T_chr).replace("J", Hand.J_chr).replace("Q", Hand.Q_chr).replace("K", Hand.K_chr).replace("A", Hand.A_chr)
        return Hand(hand_type=hand_type, cards=cards, bid=int(bid_str))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for i, hand in enumerate(sorted([Hand.from_string(line) for line in puzzle_input]), start=1):
        print(f"Hand {i} = {hand} ")
        solution += i * hand.bid
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
