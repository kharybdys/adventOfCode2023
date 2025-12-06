import re
from collections.abc import Generator

from advent.registry import register_solver
from advent.utils.range import InclusiveRange
from advent.utils.solver import split_in_groups_separated_by_empty_line

FRESH_INGREDIENT_RANGE_PATTERN = re.compile(r"(?P<id_start>\d+)-(?P<id_end>\d+)")


def parse_fresh_ranges(lines: list[str]) -> Generator[InclusiveRange, None, None]:
    for line in lines:
        match = FRESH_INGREDIENT_RANGE_PATTERN.fullmatch(line)
        yield InclusiveRange(start=int(match.group("id_start")), stop=int(match.group("id_end")))


def check_freshness(ingredient_id: int, fresh_ranges: list[InclusiveRange]) -> bool:
    for fresh_range in fresh_ranges:
        if fresh_range.within(ingredient_id):
            return True
        elif fresh_range.after(ingredient_id):
            return False


@register_solver(year="2025", key="5", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0

    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    fresh_ranges = list(sorted(parse_fresh_ranges(next(input_generator)), key=lambda r: r.start))

    for id_str in next(input_generator):
        ingredient_id = int(id_str)
        if check_freshness(ingredient_id, fresh_ranges):
            solution += 1

    print(f"Solution is {solution}")


@register_solver(year="2025", key="5", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(f"Solution is TBD")
