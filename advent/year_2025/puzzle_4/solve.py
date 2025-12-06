from collections.abc import Generator

from advent.registry import register_solver
from advent.utils.enums import PrintEnum
from advent.utils.grid import Grid, Coords


class TileStatus(PrintEnum):
    PAPER = "PAPER", "@"
    EMPTY = "EMPTY", "."


TileGrid = Grid[TileStatus]


def generate_eight_neighbours(from_coords: Coords) -> Generator[Coords, None, None]:
    for diff_x in range(-1, 2):
        for diff_y in range(-1, 2):
            if diff_x != 0 or diff_y != 0:
                yield Coords(x=from_coords.x + diff_x, y=from_coords.y + diff_y)


@register_solver(year="2025", key="4", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    solution = 0

    for x, y in grid.all_coords_for({TileStatus.PAPER}):
        paper_neighbours = 0
        for neighbour in generate_eight_neighbours(Coords(x=x, y=y)):
            if grid.value_at_or(neighbour.x, neighbour.y, default=TileStatus.EMPTY) == TileStatus.PAPER:
                paper_neighbours += 1
        if paper_neighbours < 4:
            solution += 1

    print(f"Solution is {solution}")


@register_solver(year="2025", key="4", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    solution = 0
    paper_removed = True

    while paper_removed:
        paper_removed = False
        for x, y in grid.all_coords_for({TileStatus.PAPER}):
            paper_neighbours = 0
            for neighbour in generate_eight_neighbours(Coords(x=x, y=y)):
                if grid.value_at_or(neighbour.x, neighbour.y, default=TileStatus.EMPTY) == TileStatus.PAPER:
                    paper_neighbours += 1
            if paper_neighbours < 4:
                solution += 1
                grid.set_value_at(x, y, TileStatus.EMPTY)
                paper_removed = True

    print(f"Solution is {solution}")
