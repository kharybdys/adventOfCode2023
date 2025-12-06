from collections.abc import Generator

from registry import register_solver
from utils import Grid, PrintEnum, Coords, shortest_path_analysis, Direction


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    WALL = "WALL", "#"
    START = "START", "S"
    END = "END", "E"


TileGrid = Grid[TileStatus]


def generate_all_coords_within_cheat_distance(
        grid: TileGrid,
        max_cheat_distance: int,
        start_coords: Coords,
) -> Generator[tuple[Coords, int], None, None]:
    # Should it be a requirement that at least one of the intermediate coordinates is a wall?
    for distance in range(2, max_cheat_distance + 1):
        for side_distance in range(distance):
            for direction in Direction.all():
                new_coords = direction.next_coords(*start_coords, steps=distance - side_distance)
                final_coords = Coords(*direction.cw.next_coords(*new_coords, steps=side_distance))
                if grid.value_at_or(*final_coords, default=TileStatus.WALL) != TileStatus.WALL:
                    yield final_coords, distance


def find_all_cheats(grid: TileGrid, max_cheat_distance: int) -> Generator[int, None, None]:
    end_coords = list(grid.all_coords_for({TileStatus.END}))
    if len(end_coords) != 1:
        raise ValueError("More than one end tile in the grid")

    coords_visited: dict[Coords, int] = shortest_path_analysis(grid=grid,
                                                               start_tile=TileStatus.START,
                                                               wall_tile=TileStatus.WALL,
                                                               )
    max_path_length = coords_visited[Coords(*end_coords[0])]
    print(f"{max_path_length=}, {coords_visited=}")
    for coords, length in coords_visited.items():
        if length < max_path_length:
            for new_coords, cheat_length in generate_all_coords_within_cheat_distance(grid, max_cheat_distance, coords):
                if coords_visited.get(new_coords, 0) > length + cheat_length:
                    print(f"Yielding cheat from {coords} to {new_coords}: {coords_visited[new_coords] - length - cheat_length}")
                    yield coords_visited[new_coords] - length - cheat_length


def solve(puzzle_input: list[str], cut_off: int, max_cheat_distance: int):
    print(puzzle_input)

    grid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    solution = len(list(filter(lambda i: i >= cut_off, find_all_cheats(grid, max_cheat_distance))))
    print(f"Solution is {solution}")


@register_solver(year="2024", key="20", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    cut_off = 1 if example else 100
    solve(puzzle_input, cut_off, 2)


@register_solver(year="2024", key="20", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    cut_off = 50 if example else 100
    solve(puzzle_input, cut_off, 20)
