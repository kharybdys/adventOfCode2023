import re

from advent.registry import register_solver

PATTERN = re.compile(r"\D*")


def parse_line(line: str) -> int:
    digits = list(filter(bool, PATTERN.split(line)))
    print(f"{line=}, {digits=}")
    result = int(f"{digits[0]}{digits[-1]}")
    print(f"{result=}")
    return result


@register_solver(year="2023", key="1", variation="a")
def solve(puzzle_input: list[str], example: bool) -> None:
    solution = sum(map(parse_line, puzzle_input))
    print(f"Solution is {solution}")
