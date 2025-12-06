import re
from collections.abc import Sequence
from functools import cache

from registry import register_solver
from advent.utils.solver import split_in_groups_separated_by_empty_line


def extract_towels(lines: list[str]) -> tuple[str]:
    if len(lines) != 1:
        raise ValueError(f"Invalid towels input, should be only one line: {lines}")
    return tuple(lines[0].split(", "))


def extract_towels_pattern(towels: Sequence[str]) -> str:
    return "|".join(f"({towel})" for towel in towels)


@register_solver(year="2024", key="19", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    towel_pattern = re.compile(f"^({extract_towels_pattern(extract_towels(next(input_generator)))})+$")
    solution = 0
    for line in next(input_generator):
        if towel_pattern.fullmatch(line):
            solution += 1
        else:
            print(f"No match for {line}")

    print(f"Solution is {solution}")


@cache
def count_towel_patterns(line: str, towels: tuple[str], towel_pattern: re.Pattern) -> int:
    # Stop the recursion
    if line == "":
        return 1
    # Recurse
    result = 0
    if towel_pattern.match(line):
        for towel in towels:
            if line.startswith(towel):
                result += count_towel_patterns(line[len(towel):], towels, towel_pattern)
    return result


@register_solver(year="2024", key="19", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    towels = extract_towels(next(input_generator))
    towel_pattern = re.compile(extract_towels_pattern(towels))
    full_towel_pattern = re.compile(f"^({extract_towels_pattern(towels)})+$")
    solution = 0
    for line in next(input_generator):
        if full_towel_pattern.fullmatch(line):
            solution += count_towel_patterns(line, towels, towel_pattern)
            print(f"Solution is {solution} after {line}")
        else:
            print(f"Discarding {line} because of no solutions")
    print(f"Solution is {solution}")
