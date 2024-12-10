from collections import defaultdict
from collections.abc import Generator

from registry import register_solver
from utils import PrintEnum, Grid, Direction


class TileStatus(PrintEnum):
    H_0 = 0, "0"
    H_1 = 1, "1"
    H_2 = 2, "2"
    H_3 = 3, "3"
    H_4 = 4, "4"
    H_5 = 5, "5"
    H_6 = 6, "6"
    H_7 = 7, "7"
    H_8 = 8, "8"
    H_9 = 9, "9"


TileGrid = Grid[TileStatus]


def find_coords_for(grid: TileGrid, tile_to_find: TileStatus) -> Generator[tuple[int, int], None, None]:
    for x, y, tile in grid.coords_iterator:
        if tile == tile_to_find:
            yield x, y


@register_solver(year="2024", key="10", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    # BFS
    boundary: dict[tuple[int, int], set[tuple, tuple]] = {coords: {coords} for coords in find_coords_for(grid, TileStatus.H_9)}
    print(f"Starting boundary (all 9's) is {boundary}")
    for index in range(8, -1, -1):
        new_boundary: dict[tuple[int, int], set[tuple, tuple]] = defaultdict(set)
        for coords, trail_ends in boundary.items():
            for direction in Direction.all():
                new_x, new_y = direction.next_coords(*coords)
                if grid.value_at_or(new_x, new_y, default=TileStatus.H_9).value == index:
                    new_boundary[(new_x, new_y)].update(trail_ends)
        boundary = new_boundary
        print(f"Boundary after index {index} is {boundary}")
    print(f"Solution is {sum(map(len, boundary.values()))}")


@register_solver(year="2024", key="10", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    # Fun fact, I originally had solved part A as if it should've been counting ratings

    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    # BFS
    boundary: dict[tuple[int, int], int] = {coords: 1 for coords in find_coords_for(grid, TileStatus.H_0)}
    print(f"Starting boundary (all 0's) is {boundary}")
    for index in range(1, 10):
        new_boundary: dict[tuple[int, int], int] = defaultdict(int)
        for coords, value in boundary.items():
            for direction in Direction.all():
                new_x, new_y = direction.next_coords(*coords)
                if grid.value_at_or(new_x, new_y, default=TileStatus.H_0).value == index:
                    new_boundary[(new_x, new_y)] += value
        boundary = new_boundary
        print(f"Boundary after index {index} is {boundary}")
    print(f"Solution is {sum(boundary.values())}")
