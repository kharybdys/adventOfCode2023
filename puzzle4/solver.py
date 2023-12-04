import re
from dataclasses import dataclass
from typing import ClassVar, Self


@dataclass
class Card:
    card_id: int
    winning_numbers: set[int]
    numbers: set[int]

    PATTERN: ClassVar[re.Pattern] = re.compile(r"Card\s+(\d+):\s+([\d\s]+)\s+\|\s+([\d\s]+)\s*")

    @staticmethod
    def from_line(line: str) -> Self:
        if match := Card.PATTERN.fullmatch(line):
            card_id = match[1]
            winning = match[2]
            nums = match[3]
            return Card(card_id=int(card_id),
                        winning_numbers=set(int(win) for win in winning.split()),
                        numbers=set(int(num) for num in nums.split())
                        )
        else:
            raise ValueError(f"Invalid card definition: {line}")

    def num_winning_cards(self) -> int:
        wins = self.winning_numbers.intersection(self.numbers)
        return len(wins)

    def power_value(self) -> int:
        if wins:= self.num_winning_cards():
            return 2**(wins-1)
        else:
            return 0


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    cards = [Card.from_line(line) for line in puzzle_input]
    solution = sum(card.power_value() for card in cards)
    print(solution)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
