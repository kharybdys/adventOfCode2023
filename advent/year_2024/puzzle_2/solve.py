import re
from collections.abc import Generator

from advent.registry import register_solver

PATTERN = re.compile(r"\D+")


def parse_line(line: str) -> list[int]:
    levels = list(map(int, filter(bool, PATTERN.split(line))))
    print(f"{line=}, {levels=}")
    return levels


def calculate_differences(levels: list[int]) -> Generator[int, None, None]:
    previous_level = levels[0]
    for level in levels[1:]:
        yield level - previous_level
        previous_level = level


POS_DIFFERENCES = {1, 2, 3}
NEG_DIFFERENCES = {-1, -2, -3}


def valid_levels(level_differences: set[int]) -> int:
    if level_differences <= POS_DIFFERENCES or level_differences <= NEG_DIFFERENCES:
        return 1
    return 0


@register_solver(year="2024", key="2", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    levels_list = list(map(parse_line, puzzle_input))
    level_differences_list = list(map(set, map(calculate_differences, levels_list)))
    solution = sum(map(valid_levels, level_differences_list))
    print(f"Solution is {solution}")


def valid_levels_dampened(levels: list[int]) -> int:
    full_diffs = set(calculate_differences(levels))
    if valid_levels(full_diffs):
        return 1
    for i in range(0, len(levels)):
        diffs = set(calculate_differences(levels[0:i] + levels[i+1:]))
        if valid_levels(diffs):
            return 1
    return 0


@register_solver(year="2024", key="2", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    levels_list = list(map(parse_line, puzzle_input))
    solution = sum(map(valid_levels_dampened, levels_list))
    print(f"Solution is {solution}")
