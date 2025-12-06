import re
from collections.abc import Generator
from itertools import batched
from math import sqrt

from advent.registry import register_solver
from advent.utils.all_equal import all_equal


def generate_divisors(nr: int) -> Generator[int, None, None]:
    for i in range(1, int(sqrt(nr)) + 1):
        if nr % i == 0:
            if i != nr:
                yield i
            if nr // i != nr:
                yield nr // i


def invalid_id_b(id_to_check: int) -> bool:
    id_str = str(id_to_check)
    for divisor in generate_divisors(len(id_str)):
        parts = batched(id_str, n=divisor)
        if all_equal(parts):
            return True
    return False


def invalid_id_a(id_to_check: int) -> bool:
    id_str = str(id_to_check)
    if len(id_str) % 2 != 0:
        return False
    halfway = len(id_str) // 2
    return id_str[0:halfway] == id_str[halfway:]


ID_RANGE_PATTERN = re.compile(r"(?P<id_start>\d+)-(?P<id_end>\d+)")


def generate_ids(line: str) -> Generator[int, None, None]:
    for id_range in line.split(","):
        match = ID_RANGE_PATTERN.fullmatch(id_range)
        id_end = int(match.group("id_end"))
        id_start = int(match.group("id_start"))
        for id_to_check in range(id_start, id_end + 1):
            yield id_to_check


@register_solver(year="2025", key="2", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    if len(puzzle_input) != 1:
        raise ValueError("Puzzle input for 2025, 2 is expected to be a single line")

    for id_to_check in generate_ids(puzzle_input[0]):
        if invalid_id_a(id_to_check):
            solution += id_to_check

    print(f"Solution is {solution}")


@register_solver(year="2025", key="2", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    if len(puzzle_input) != 1:
        raise ValueError("Puzzle input for 2025, 2 is expected to be a single line")

    for id_to_check in generate_ids(puzzle_input[0]):
        if invalid_id_b(id_to_check):
            print(f"Invalid: {id_to_check=}")
            solution += id_to_check

    print(f"Solution is {solution}")
