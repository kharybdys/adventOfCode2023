from collections import namedtuple
from collections.abc import Generator
from itertools import chain

from registry import register_solver
from utils import PrintEnum, Grid, Direction, split_in_groups_separated_by_empty_line


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    WALL = "WALL", "#"
    ROBOT_START = "ROBOT_START", "@"
    BOX = "BOX", "O"
    BOX_LEFT = "BOX_LEFT", "["
    BOX_RIGHT = "BOX_RIGHT", "]"


TileGrid = Grid[TileStatus]

Coords = namedtuple("Coords", ["x", "y"])


def gps_at(x: int, y: int, tile: TileStatus) -> int:
    if tile in [TileStatus.BOX, TileStatus.BOX_LEFT]:
        return 100 * y + x
    else:
        return 0


def calculate_gps(grid: TileGrid) -> int:
    return sum(gps_at(x, y, tile) for x, y, tile in grid.coords_iterator)


def find_start_coords(grid: TileGrid) -> Coords:
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.ROBOT_START:
            grid.set_value_at(x, y, TileStatus.EMPTY)
            return Coords(x, y)
    raise ValueError("Grid does not contain a ROBOT_START position")


def possibly_move_to(grid: TileGrid, coords_to_check: set[Coords], direction: Direction) -> bool:
    print(f"Checking {coords_to_check} for {direction}")
    new_coords_to_check = set()
    for coords in coords_to_check:
        match grid.value_at(*coords):
            case TileStatus.WALL:
                return False
            case TileStatus.BOX:
                new_x, new_y = direction.next_coords(*coords)
                new_coords_to_check.add(Coords(new_x, new_y))
            case TileStatus.BOX_LEFT | TileStatus.BOX_RIGHT if direction.horizontal:
                new_x, new_y = direction.next_coords(*coords)
                new_coords_to_check.add(Coords(new_x, new_y))
            case TileStatus.BOX_RIGHT if direction.vertical:
                new_x, new_y = direction.next_coords(*coords)
                new_coords_to_check.add(Coords(new_x, new_y))
                # And for the tile to the west of this
                new_x, new_y = Direction.WEST.next_coords(*coords)
                new_x, new_y = direction.next_coords(new_x, new_y)
                new_coords_to_check.add(Coords(new_x, new_y))
            case TileStatus.BOX_LEFT if direction.vertical:
                new_x, new_y = direction.next_coords(*coords)
                new_coords_to_check.add(Coords(new_x, new_y))
                # And for the tile to the east of this
                new_x, new_y = Direction.EAST.next_coords(*coords)
                new_x, new_y = direction.next_coords(new_x, new_y)
                new_coords_to_check.add(Coords(new_x, new_y))
    if not new_coords_to_check or possibly_move_to(grid, new_coords_to_check, direction):
        # Move everything into our own coords_to_check, they will now all be empty:
        for coords in coords_to_check:
            if grid.value_at(*coords) != TileStatus.EMPTY:
                grid.print_grid(lambda t: t.str_repr)
                raise ValueError(f"Grid at {coords} is not empty, but {grid.value_at(*coords)}")
            old_x, old_y = direction.opposite.next_coords(*coords)
            grid.set_value_at(*coords, value=grid.value_at(old_x, old_y))
            grid.set_value_at(old_x, old_y, value=TileStatus.EMPTY)
        return True


def walk_the_robot(grid: TileGrid, instructions: list[str], example: bool):
    coords = find_start_coords(grid)
    for instruction in chain(*instructions):
        if example:
            grid.print_grid(lambda t: t.str_repr)
        direction = Direction.from_char(instruction).opposite
        print(f"Instruction for {direction}, from coords {coords}")
        new_x, new_y = direction.next_coords(*coords)
        if possibly_move_to(grid, {Coords(new_x, new_y)}, direction):
            coords = Coords(new_x, new_y)
        print(f"After direction {direction}, coords: {coords}")

    grid.print_grid(lambda t: t.str_repr)


@register_solver(year="2024", key="15", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    grid: TileGrid = Grid.from_lines(next(input_generator), TileStatus.from_char)
    walk_the_robot(grid, next(input_generator), example)
    print(f"Solution is {calculate_gps(grid)}")


def widen(char: str) -> str:
    match char:
        case ".":
            return ".."
        case "@":
            return "@."
        case "O":
            return "[]"
        case "#":
            return "##"
        case a:
            raise ValueError(f"Got unknown char {a}")


def widen_lines(lines: list[str]) -> Generator[str, None, None]:
    for line in lines:
        yield "".join(widen(char) for char in line)


@register_solver(year="2024", key="15", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    input_generator = split_in_groups_separated_by_empty_line(puzzle_input)
    grid: TileGrid = Grid.from_lines(list(widen_lines(next(input_generator))), TileStatus.from_char)
    walk_the_robot(grid, next(input_generator), example)
    print(f"Solution is {calculate_gps(grid)}")
