from collections import defaultdict

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


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
