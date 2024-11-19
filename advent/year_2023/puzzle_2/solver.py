from advent.year_2023.puzzle_2.base import Game
from registry import register_solver

SACK_CONTENTS_A = {"red": 12, "green": 13, "blue": 14}


@register_solver(year="2023", key="2", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    games = [Game.from_string(puzzle) for puzzle in puzzle_input]
    solution = sum(map(lambda g: g.id, filter(lambda g: g.possible(SACK_CONTENTS_A), games)))
    print(f"{solution=}")


@register_solver(year="2023", key="2", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    games = [Game.from_string(puzzle) for puzzle in puzzle_input]
    solution = sum(map(lambda g: g.power_value(), games))
    print(f"{solution=}")
