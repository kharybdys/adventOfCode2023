from copy import copy
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar, Self


@dataclass(frozen=True)
class NonogramPattern:
    target_pattern: str
    black_pattern: list[int] = field(default_factory=list)
    white_pattern: list[int] = field(default_factory=list)
    EMPTY: ClassVar[str] = "."
    UNKNOWN: ClassVar[str] = "?"
    FILLED: ClassVar[str] = "#"

    def __repr__(self) -> str:
        return f"NonogramPattern(pattern={self.target_pattern}, partial={self.partial_string}, blacks={self.black_pattern}, whites={self.white_pattern})"

    @cached_property
    def total_whites_possible(self) -> int:
        return len(self.target_pattern) - sum(self.black_pattern) - len(self.black_pattern) + 1

    @cached_property
    def remaining_whites_possible(self) -> int:
        if len(self.white_pattern) == 0:
            correction = 0
        elif len(self.white_pattern) == len(self.black_pattern) + 1:
            correction = 2
        else:
            correction = 1
        return self.total_whites_possible - sum(self.white_pattern) + len(self.white_pattern) - correction

    @cached_property
    def first_or_last(self) -> bool:
        return len(self.white_pattern) == 0 or len(self.white_pattern) >= len(self.black_pattern)

    @cached_property
    def partial_string(self) -> str:
        chars = []
        for index, white_length in enumerate(self.white_pattern):
            chars.extend([self.EMPTY] * white_length)
            if index < len(self.black_pattern):
                chars.extend([self.FILLED] * self.black_pattern[index])
        if not self.first_or_last:
            chars.append(self.EMPTY)
        return "".join(chars)

    @cached_property
    def matches(self) -> bool:
        for index, char in enumerate(self.partial_string):
            if char == self.UNKNOWN or self.target_pattern[index] == self.UNKNOWN:
                continue
            elif char == self.FILLED and self.target_pattern[index] == self.FILLED:
                continue
            elif char == self.EMPTY and self.target_pattern[index] == self.EMPTY:
                continue
            else:
                return False
        return True

    @cached_property
    def completed(self) -> bool:
        return len(self.white_pattern) == len(self.black_pattern) + 1

    @cached_property
    def valid(self) -> bool:
        return self.completed and self.remaining_whites_possible == 0 and self.matches

    def copy_and_next_white_length(self, next_white: int) -> Self:
        return NonogramPattern(target_pattern=self.target_pattern, black_pattern=copy(self.black_pattern), white_pattern=copy(self.white_pattern) + [next_white])


def to_nonogram_pattern(line: str, multiplier: int) -> NonogramPattern:
    parts_string, pattern_string = line.split()
    parts_string = "?".join([parts_string] * multiplier)

    pattern_string = ",".join([pattern_string] * multiplier)
    pattern = list(map(int, pattern_string.split(",")))
    return NonogramPattern(target_pattern=parts_string, black_pattern=pattern)
