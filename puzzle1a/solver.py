import re


PATTERN = re.compile(r"\D*")


def parse_line(line: str) -> int:
    digits = list(filter(bool, PATTERN.split(line)))
    print(f"{line=}, {digits=}")
    result = int(f"{digits[0]}{digits[-1]}")
    print(f"{result=}")
    return result


def solve(puzzle_input: list[str]) -> None:
    solution = sum(map(parse_line, puzzle_input))
    print(f"Solution is {solution}")
