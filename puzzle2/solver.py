from puzzle2.base import Game


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    games = [Game.from_string(puzzle) for puzzle in puzzle_input]
    print(games)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
