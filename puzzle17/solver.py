from dataclasses import dataclass

from utils import Direction, Grid


@dataclass
class Attempt:
    x: int
    y: int
    entry: Direction
    cost: int
    straight_steps_taken: int = 0


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid = Grid.from_lines(puzzle_input, int)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
