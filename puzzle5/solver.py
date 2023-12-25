from puzzle5.base import ProblemA, ProblemB


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    problem = ProblemA.from_string(puzzle_input)
    print(problem.solve())


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    problem = ProblemB.from_string(puzzle_input)
    print(problem.solve())
