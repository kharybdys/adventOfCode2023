from collections import defaultdict
from typing import Generator

from puzzle16.grid import Grid, Beam
from utils import Direction


def print_grid_and_beams(grid: Grid, beams_by_coords: dict[tuple[int, int], set[Direction]]):
    def print_char_at(x: int, y: int) -> str:
        tile = grid.status_at(x, y)
        beams = beams_by_coords.get((x, y), [])
        if not tile.empty() or not beams:
            return tile.str_repr
        else:
            if len(beams) == 1:
                return beams.pop().str_repr
            else:
                return str(len(beams))

    for y in range(0, grid.height):
        print("".join(print_char_at(x, y) for x in range(0, grid.width)))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid = Grid.from_lines(puzzle_input)
    beams_by_coords = grid.generate_beams_by_coords(Beam(0, 0, Direction.WEST))
    print_grid_and_beams(grid, beams_by_coords=beams_by_coords)
    print(len(beams_by_coords.keys()))


def calculate_energization_for_all_options(grid: Grid) -> Generator[int, None, None]:
    options: list[Beam] = []
    options.extend(Beam(x, 0, Direction.NORTH) for x in range(0, grid.width))
    options.extend(Beam(0, y, Direction.WEST) for y in range(0, grid.height))
    options.extend(Beam(x, grid.height - 1, Direction.SOUTH) for x in range(0, grid.width))
    options.extend(Beam(grid.width - 1, y, Direction.EAST) for y in range(0, grid.height))
    for option in options:
        beams_by_coords = grid.generate_beams_by_coords(option)
        yield len(beams_by_coords.keys())


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid = Grid.from_lines(puzzle_input)
    print(max(calculate_energization_for_all_options(grid)))
