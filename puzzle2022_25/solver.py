from puzzle2022_25.base import SNAFUNumber


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    solution = sum((SNAFUNumber.parse(puzzle) for puzzle in puzzle_input), start=SNAFUNumber.parse("0"))
    print(f"{solution}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
