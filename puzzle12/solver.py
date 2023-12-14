import re
from dataclasses import dataclass, field
from typing import Self, ClassVar


@dataclass
class Line:
    parts: list[str] = field(default_factory=list)
    pattern: list[int] = field(default_factory=list)
    PARSER_PATTERN: ClassVar[re.Pattern] = re.compile(r"\.+")

    @staticmethod
    def from_string(string: str) -> Self:
        parts_string, pattern_string = string.split()
        parts = Line.PARSER_PATTERN.split(parts_string)
        pattern = list(map(int, pattern_string.split(",")))
        return Line(parts=parts, pattern=pattern)


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
