import re
from collections.abc import Generator
from dataclasses import dataclass
from typing import Self, ClassVar

from advent.registry import register_solver


@dataclass
class SumCandidate:
    outcome: int
    numbers: list[int]

    _pattern: ClassVar[re.Pattern] = re.compile(r"\s*(?P<outcome>\d+): (?P<numbers>.+)\s*")

    @classmethod
    def from_line(cls, line: str) -> Self:
        if result := cls._pattern.fullmatch(line):
            return cls(
                outcome=int(result["outcome"]),
                numbers=[int(value) for value in result["numbers"].split(" ")]
            )
        else:
            raise ValueError(f"Cannot parse line {line}")

    def deconstruct(self, simple: bool) -> Generator[Self, None, None]:
        last_number = self.numbers[-1]
        if self.outcome % last_number == 0:
            # * is an option
            yield SumCandidate(
                outcome=self.outcome // last_number,
                numbers=self.numbers[:-1]
            )
        # + is always an option
        yield SumCandidate(
            outcome=self.outcome - last_number,
            numbers=self.numbers[:-1]
        )

        if not simple:
            # Part B also allows concatenation
            pattern = re.compile(rf"(?P<new_outcome>\d+){self.numbers[-1]}")
            if result := pattern.fullmatch(str(self.outcome)):
                yield SumCandidate(
                    outcome=int(result["new_outcome"]),
                    numbers=self.numbers[:-1]
                )


def solvable(sum_candidate: SumCandidate, simple: bool) -> bool:
    print(f"Checking solvable for {sum_candidate=}, {simple=}")
    # End condition
    if len(sum_candidate.numbers) == 1:
        return sum_candidate.outcome == sum_candidate.numbers[0]
    elif sum_candidate.outcome < 0:
        return False
    else:
        # Recurse!
        return any(solvable(new_candidate, simple=simple) for new_candidate in sum_candidate.deconstruct(simple))


@register_solver(year="2024", key="7", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    sum_candidates = [SumCandidate.from_line(line) for line in puzzle_input]
    solution = sum(sum_candidate.outcome for sum_candidate in sum_candidates if solvable(sum_candidate, True))
    print(f"Solution is {solution}")


@register_solver(year="2024", key="7", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    sum_candidates = [SumCandidate.from_line(line) for line in puzzle_input]
    solution = sum(sum_candidate.outcome for sum_candidate in sum_candidates if solvable(sum_candidate, False))
    print(f"Solution is {solution}")
