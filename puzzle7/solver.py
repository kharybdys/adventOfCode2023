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
        return f"Hand[type={self.hand_type}, cards={self.cards_repr}, bid={self.bid}]"

    @property
    def cards_repr(self) -> str:
        return self.cards.replace(self.A_chr, "A").replace(self.K_chr, "K").replace(self.Q_chr, "Q").replace(self.J_chr, "J").replace(self.T_chr, "T")

    @classmethod
    def to_hand_type(cls, cards: str) -> HandType:
        cards_count = Counter(cards)
        print(f"{cards_count=}, {cards=}, {list(sorted(cards_count.values()))=}")
        if 5 in cards_count.values():
            return HandType.FIVE_OF_A_KIND
        elif 4 in cards_count.values():
            return HandType.FOUR_OF_A_KIND
        elif 3 in cards_count.values() and 2 in cards_count.values():
            return HandType.FULL_HOUSE
        elif 3 in cards_count.values():
            return HandType.THREE_OF_A_KIND
        elif [1, 2, 2] == list(sorted(cards_count.values())):
            return HandType.DOUBLE_PAIR
        elif 2 in cards_count.values():
            return HandType.PAIR
        else:
            return HandType.SINGLE_CARD

    @classmethod
    def from_string(cls, line: str) -> Self:
        orig_cards, bid_str = line.split()
        hand_type = cls.to_hand_type(orig_cards)
        cards = orig_cards.replace("T", cls.T_chr).replace("J", cls.J_chr).replace("Q", cls.Q_chr).replace("K", cls.K_chr).replace("A", cls.A_chr)
        print(f"{line=}, {hand_type.name=}")
        return cls(hand_type=hand_type, cards=cards, bid=int(bid_str))


class JokerHand(Hand):
    J_chr: ClassVar[str] = chr(ord("1") - 2)

    @classmethod
    def to_hand_type(cls, cards: str) -> HandType:
        cards_count = Counter(cards)
        joker_count = cards_count.get("J", 0)
        del cards_count["J"]
        sorted_values = sorted(cards_count.values(), reverse=True)
        highest_value = sorted_values[0] if sorted_values else 0
        print(f"{cards=}, {highest_value=}, {sorted_values=}, {joker_count=}")
        match highest_value:
            case 5:
                return HandType.FIVE_OF_A_KIND
            case 4 if joker_count == 1:
                return HandType.FIVE_OF_A_KIND
            case 4:
                return HandType.FOUR_OF_A_KIND
            case 3 if joker_count == 2:
                return HandType.FIVE_OF_A_KIND
            case 3 if joker_count == 1:
                return HandType.FOUR_OF_A_KIND
            case 3 if sorted_values[1] == 2:
                return HandType.FULL_HOUSE
            case 3:
                return HandType.THREE_OF_A_KIND
            case 2 if joker_count == 3:
                return HandType.FIVE_OF_A_KIND
            case 2 if joker_count == 2:
                return HandType.FOUR_OF_A_KIND
            case 2 if joker_count == 1 and sorted_values[1] == 2:
                return HandType.FULL_HOUSE
            case 2 if joker_count == 1:
                return HandType.THREE_OF_A_KIND
            case 2 if sorted_values[1] == 2:
                return HandType.DOUBLE_PAIR
            case 2:
                return HandType.PAIR
            case 1 if joker_count == 4:
                return HandType.FIVE_OF_A_KIND
            case 1 if joker_count == 3:
                return HandType.FOUR_OF_A_KIND
            case 1 if joker_count == 2:
                return HandType.THREE_OF_A_KIND
            case 1 if joker_count == 1:
                return HandType.PAIR
            case 1:
                return HandType.SINGLE_CARD
            case 0 if joker_count == 5:
                return HandType.FIVE_OF_A_KIND


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for i, hand in enumerate(sorted([Hand.from_string(line) for line in puzzle_input]), start=1):
        print(f"Hand {i} = {hand} ")
        solution += i * hand.bid
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = 0
    for i, hand in enumerate(sorted([JokerHand.from_string(line) for line in puzzle_input]), start=1):
        print(f"Hand {i} = {hand} ")
        solution += i * hand.bid
    print(solution)
