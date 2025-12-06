import re
from collections import Counter

from advent.registry import register_solver

PATTERN = re.compile(r"\D+")


def parse_line(line: str) -> tuple[int, int]:
    digits = list(filter(bool, PATTERN.split(line)))
    print(f"{line=}, {digits=}")
    if len(digits) != 2:
        raise ValueError(f"Invalid line for puzzle 1: {line}")
    return int(digits[0]), int(digits[1])


@register_solver(year="2024", key="1", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    two_lists = zip(*map(parse_line, puzzle_input))
    pairs = zip(*map(sorted, two_lists))
    solution = sum(map(lambda pair: abs(pair[0] - pair[1]), pairs))
    print(f"Solution is {solution}")


@register_solver(year="2024", key="1", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    two_lists = list(map(list, zip(*map(parse_line, puzzle_input))))
    count_second_list = Counter(two_lists[1])
    solution = sum(map(lambda n: n * count_second_list.get(n, 0), two_lists[0]))
    print(f"Solution is {solution}")
