from puzzle5.base import Problem


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    problem = Problem.from_string(puzzle_input)
    print(problem.solve())


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
