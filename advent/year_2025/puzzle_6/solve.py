import re
from math import prod
from functools import partial

from advent.registry import register_solver

PROBLEM_DEFINITION_PATTERN = re.compile(r"[+*0-9-]+")


@register_solver(year="2025", key="6", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = 0

    number_generators = [PROBLEM_DEFINITION_PATTERN.finditer(line) for line in puzzle_input]
    operator_generator = number_generators.pop(-1)

    while operator_match := next(operator_generator, None):
        operator = operator_match.group(0)
        if operator == "+":
            func = sum
        elif operator == "*":
            func = partial(prod, start=1)
        else:
            raise ValueError(f"Unsupported operator {operator}")
        numbers = [int(next(number_generator).group(0)) for number_generator in number_generators]
        solution += func(numbers)

    print(f"Solution is {solution}")


@register_solver(year="2025", key="6", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(f"Solution is TBD")
