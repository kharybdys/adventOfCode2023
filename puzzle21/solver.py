from collections import namedtuple
from typing import Generator

from utils import Grid, Direction, PrintEnum


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    ROCK = "ROCK", "#"
    START = "START", "S"

    def __bool__(self) -> bool:
        return self == TileStatus.ROCK


TileGrid = Grid[TileStatus]

Coords = namedtuple("Coords", ["x", "y"])


def get_start_coord(grid: TileGrid) -> tuple[int, int]:
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.START:
            return x, y


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    coords: set = set()
    coords.add(Coords(*get_start_coord(grid)))
    for step in range(0, 64):
        print(f"Beginning of {step=}, total coords: {len(coords)}")
        new_coords = set()
        for coord in coords:
            for direction in Direction.all():
                new_coord = Coords(*direction.next_coords(coord.x, coord.y))
                if grid.within_bounds(*new_coord) and not grid.value_at(*new_coord):
                    new_coords.add(new_coord)
        coords = new_coords
    print(len(coords))


def grid_value_at_wrapped(x: int, y: int, grid: TileGrid) -> TileStatus:
    lim_x = x % grid.width
    lim_y = y % grid.height
    return grid.value_at(lim_x, lim_y)


def generate_coordinates(step: int) -> Generator[tuple[int, int], None, None]:
    for current_sum in range(-step, step + 1, 2):
        if current_sum > 0:
            for x in range(0, step + 1):
                y = current_sum - x
                yield x, y
        elif current_sum < 0:
            for x in range(-step, 1):
                y = current_sum - x
                yield x, y
        else:
            half_step = step // 2
            for x in range(-half_step, half_step + 1):
                y = current_sum - x
                yield x, y


def calculate_valid_targets(start_x: int, start_y: int, grid: TileGrid, step: int) -> int:
    solution = 0
    for x, y in generate_coordinates(step):
        # print(f"Checking  {x}, {y}")
        if grid_value_at_wrapped(x=x + start_x, y=y + start_y, grid=grid) != TileStatus.ROCK:
            # print(f"Not a rock at {x + start_x}, {y + start_y}.")
            solution += 1
    return solution


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    target_step = 26501365 + 1
    # Need to check target_step * target_step options, centered on start_x, start_y
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    start_x, start_y = get_start_coord(grid)
    # Approach might still be too slow
    # More importantly, counting too many since some squares will not have been reachable due to a rock on an earlier step
    print(calculate_valid_targets(start_x, start_y, grid, step=target_step))
    for step in range(0, 6):
        print(f"{step=}: {calculate_valid_targets(start_x, start_y, grid, step=step)}")
