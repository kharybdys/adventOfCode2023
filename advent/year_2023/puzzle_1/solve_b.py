import re
from typing import Generator

from registry import register_solver

PATTERN = re.compile(r"\d|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)")


def str_to_number(string: str) -> int:
    match string:
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case "six":
            return 6
        case "seven":
            return 7
        case "eight":
            return 8
        case "nine":
            return 9
        case _:
            return int(string)


def line_to_digits(line: str) -> Generator[str, None, None]:
    for i in range(0, len(line)):
        match = PATTERN.match(line, i)
        if match:
            yield match[0]


def parse_line(line: str) -> int:
    digits = list(line_to_digits(line))
    print(f"{line=}, {digits=}")
    result = int(f"{str_to_number(digits[0])}{str_to_number(digits[-1])}")
    print(f"{result=}")
    return result


@register_solver(year="2023", key="1", variation="b")
def solve(puzzle_input: list[str], example: bool) -> None:
    solution = sum(map(parse_line, puzzle_input))
    print(f"Solution is {solution}")
