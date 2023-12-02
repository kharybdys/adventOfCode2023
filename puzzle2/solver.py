from puzzle2.base import Game

SACK_CONTENTS_A = {"red": 12, "green": 13, "blue": 14}


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    games = [Game.from_string(puzzle) for puzzle in puzzle_input]
    solution = sum(map(lambda g: g.id, filter(lambda g: g.possible(SACK_CONTENTS_A), games)))
    print(f"{solution=}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    games = [Game.from_string(puzzle) for puzzle in puzzle_input]
    solution = sum(map(lambda g: g.power_value(), games))
    print(f"{solution=}")
