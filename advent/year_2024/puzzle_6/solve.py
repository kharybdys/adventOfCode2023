from advent.registry import register_solver
from advent.utils.enums import PrintEnum, Direction
from advent.utils.grid import Grid


class TileStatus(PrintEnum):
    START_NORTH = "START_NORTH", "^"
    PATH = "PATH", "."
    WALL = "WALL", "#"


TileGrid = Grid[TileStatus]


def find_start_coords(grid: TileGrid) -> tuple[int, int, Direction]:
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.START_NORTH:
            return x, y, Direction.NORTH
    raise ValueError("No starting coordinates found")


def next_step_simple(grid: TileGrid, x: int, y: int, direction: Direction) -> tuple[int, int, Direction]:
    new_x, new_y = direction.next_coords(x, y)
    next_tile = grid.value_at_or(new_x, new_y, default=TileStatus.PATH)
    if next_tile == TileStatus.WALL:
        return x, y, direction.cw
    else:
        return new_x, new_y, direction


@register_solver(year="2024", key="6", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    coords_passed: set[tuple[int, int]] = set()
    x, y, direction = find_start_coords(grid)
    while grid.within_bounds(x, y):
        coords_passed.add((x, y))
        x, y, direction = next_step_simple(grid, x, y, direction)
    print(f"Solution is {len(coords_passed)}")


def check_loop(grid: TileGrid,
               coords_passed: set[tuple[int, int, Direction]],
               start_x: int,
               start_y: int,
               direction: Direction
               ) -> bool:
    x, y = start_x, start_y

    loop_coords_passed: set[tuple[int, int, Direction]] = set()

    while grid.within_bounds(x, y):
        loop_coords_passed.add((x, y, direction))

        x, y, direction = next_step_simple(grid, x, y, direction)

        if (x, y, direction) in coords_passed:
            return True
        if (x, y, direction) in loop_coords_passed:
            return True

    return False


def wall_possible(grid: TileGrid, x: int, y: int, coords_passed: set[tuple[int, int, Direction]]) -> bool:
    if grid.value_at_or(x, y, default=TileStatus.PATH) == TileStatus.WALL:
        return False
    if not grid.within_bounds(x, y):
        return False
    walls = {(x, y, Direction.NORTH), (x, y, Direction.WEST), (x, y, Direction.SOUTH), (x, y, Direction.EAST)}
    if walls.intersection(coords_passed):
        return False
    return True


@register_solver(year="2024", key="6", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)

    print(f"{grid.width=}, {grid.height=}, size: {grid.width * grid.height}, non-walls: {len(list(tile for tile in grid.tiles_iterator if tile != TileStatus.WALL))}")
    blocks_possible: set[tuple[int, int]] = set()
    coords_passed: set[tuple[int, int, Direction]] = set()

    start_x, start_y, direction = find_start_coords(grid)

    x, y = start_x, start_y

    while grid.within_bounds(x, y):

        coords_passed.add((x, y, direction))
        wall_x, wall_y = direction.next_coords(x, y)

        if wall_possible(grid, wall_x, wall_y, coords_passed):
            grid.set_value_at(wall_x, wall_y, value=TileStatus.WALL)

            if check_loop(grid, coords_passed, x, y, direction):
                # Obstacle possible
                blocks_possible.add((wall_x, wall_y))

            grid.set_value_at(wall_x, wall_y, value=TileStatus.PATH)

        x, y, direction = next_step_simple(grid, x, y, direction)

    if (start_x, start_y) in blocks_possible:
        blocks_possible.remove((start_x, start_y))

    print(f"{blocks_possible=}")
    print(f"Solution is {len(blocks_possible)}")
