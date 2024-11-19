from advent.year_2023.puzzle_5.base import ProblemA, ProblemB
from registry import register_solver


@register_solver(year="2023", key="5", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    problem = ProblemA.from_string(puzzle_input)
    print(problem.solve())


@register_solver(year="2023", key="5", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    problem = ProblemB.from_string(puzzle_input)
    print(problem.solve())
