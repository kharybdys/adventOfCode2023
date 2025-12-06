import re
from collections import namedtuple
from dataclasses import dataclass
from typing import Self, ClassVar

from advent.registry import register_solver
from advent.utils.solver import split_in_groups_separated_by_empty_line

Coords = namedtuple("Coords", ["x", "y"])


def ceil_div(a: int, b: int) -> int:
    return -(a // -b)


@dataclass
class ClawMachine:
    button_a: Coords
    button_b: Coords
    prize: Coords
    A_PATTERN: ClassVar[re.Pattern] = re.compile(r"Button A: X\+(?P<x>\d+), Y\+(?P<y>\d+)")
    B_PATTERN: ClassVar[re.Pattern] = re.compile(r"Button B: X\+(?P<x>\d+), Y\+(?P<y>\d+)")
    PRIZE_PATTERN: ClassVar[re.Pattern] = re.compile(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)")
    A_COST: ClassVar[int] = 3
    B_COST: ClassVar[int] = 1
    PRIZE_SHIFT: ClassVar[int] = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        assert len(lines) == 3
        button_a: Coords | None = None
        button_b: Coords | None = None
        prize: Coords | None = None
        for line in lines:
            if line_match := cls.A_PATTERN.fullmatch(line):
                button_a = Coords(x=int(line_match["x"]), y=int(line_match["y"]))
            if line_match := cls.B_PATTERN.fullmatch(line):
                button_b = Coords(x=int(line_match["x"]), y=int(line_match["y"]))
            if line_match := cls.PRIZE_PATTERN.fullmatch(line):
                prize = Coords(
                    x=int(line_match["x"]) + cls.PRIZE_SHIFT,
                    y=int(line_match["y"]) + cls.PRIZE_SHIFT
                )
        if button_a and button_b and prize:
            return cls(button_a=button_a,
                       button_b=button_b,
                       prize=prize)
        else:
            raise ValueError(f"Couldn't get one of button_a, button_b or prize from lines: {lines}")

    def calculate_tokens_needed(self, max_steps: int) -> int:
        print(f"{self}")
        # button_b is cheapest so we want to use as much of those as possible. So start with using only those:
        presses_b = min(self.prize.x // self.button_b.x, self.prize.y // self.button_b.y)
        remaining = Coords(
            x=self.prize.x - presses_b * self.button_b.x,
            y=self.prize.y - presses_b * self.button_b.y
        )
        print(f"At {presses_b=}, {remaining=}")
        presses_a = max(ceil_div(remaining.x, self.button_a.x), ceil_div(remaining.y, self.button_a.y))
        remaining = Coords(
            x=remaining.x - presses_a * self.button_a.x,
            y=remaining.y - presses_a * self.button_a.y
        )
        print(f"At {presses_b=}, {presses_a=}, {remaining=}")
        while remaining != Coords(0, 0) and presses_b > 0:
            # reduce nr of b presses to get remaining.x and y >= 0
            correction_b = max(ceil_div(-1 * remaining.x, self.button_b.x), ceil_div(-1 * remaining.y, self.button_b.y))
            presses_b -= correction_b
            remaining = Coords(
                x=remaining.x + correction_b * self.button_b.x,
                y=remaining.y + correction_b * self.button_b.y
            )
            print(f"At {presses_b=}, {presses_a=}, {remaining=}")
            if remaining != Coords(0, 0) and presses_b > 0:
                # increase nr of a presses to get remaining.x and y <= 0
                correction_a = max(ceil_div(remaining.x, self.button_a.x), ceil_div(remaining.y, self.button_a.y))
                presses_a += correction_a
                remaining = Coords(
                    x=remaining.x - correction_a * self.button_a.x,
                    y=remaining.y - correction_a * self.button_a.y
                )
                print(f"At {presses_b=}, {presses_a=}, {remaining=}")

        if remaining == Coords(0, 0):
            print(f"Solution: {presses_b=}, {presses_a=}, {remaining=}")
            assert self.prize.x == presses_b * self.button_b.x + presses_a * self.button_a.x
            assert self.prize.y == presses_b * self.button_b.y + presses_a * self.button_a.y

            return presses_a * self.A_COST + presses_b * self.B_COST
        else:
            print("No solution possible")
            return 0


class ExpensiveClawMachine(ClawMachine):
    PRIZE_SHIFT: ClassVar[int] = 10000000000000


@register_solver(year="2024", key="13", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(map(lambda c: c.calculate_tokens_needed(100), map(ClawMachine.from_lines, split_in_groups_separated_by_empty_line(puzzle_input))))
    print(f"Solution is {solution}")


@register_solver(year="2024", key="13", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(map(lambda c: c.calculate_tokens_needed(100), map(ExpensiveClawMachine.from_lines, split_in_groups_separated_by_empty_line(puzzle_input))))
    print(f"Solution is {solution}")
