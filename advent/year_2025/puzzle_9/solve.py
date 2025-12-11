from collections import deque
from itertools import combinations

from advent.registry import register_solver
from advent.utils.enums import PrintEnum, Direction
from advent.utils.grid import Coords, Grid
from advent.utils.range import InclusiveRange


def parse_line(line: str) -> Coords:
    parts = line.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid line, expected two parts separated by comma: {line}")
    return Coords(x=int(parts[0]), y=int(parts[1]))


@register_solver(year="2025", key="9", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    coords = list(map(parse_line, puzzle_input))
    solution = 0
    for corner_1, corner_2 in combinations(coords, 2):
        size = abs((corner_1.x - corner_2.x) + 1) * abs((corner_1.y - corner_2.y) + 1)
        if size > solution:
            solution = size
    print(f"Solution is {solution}")


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    RED = "RED", "#"
    OUTSIDE = "OUTSIDE", "o"
    INSIDE = "INSIDE", "X"


TileGrid = Grid[TileStatus]


def create_grid(puzzle_input: list[str]) -> TileGrid:
    coords = list(map(parse_line, puzzle_input))
    min_x = min(coord.x for coord in coords)
    max_x = max(coord.x for coord in coords)
    min_y = min(coord.y for coord in coords)
    max_y = max(coord.y for coord in coords)
    if min_x < 0:
        raise ValueError("Cannot work with negative x coordinates")
    if min_y < 0:
        raise ValueError("Cannot work with negative y coordinates")

    print(f"Creating grid with sizes {max_x + 2} and {max_y + 2}")
    grid = Grid.from_size(max_x + 2, max_y + 2, TileStatus.EMPTY)
    # Fill in the boundaries
    coord_iterator = iter(coords)
    last_coord = coords[-1]
    grid.set_value_at(last_coord.x, last_coord.y, TileStatus.RED)
    while coord := next(coord_iterator, None):
        grid.set_value_at(coord.x, coord.y, TileStatus.RED)
        if coord == last_coord:
            raise ValueError(f"Same coordinates repeat, should not be possible: {coord}")
        if coord.x == last_coord.x:
            # Fill vertical
            for y in range(min(coord.y, last_coord.y), max(coord.y, last_coord.y) + 1):
                if grid.value_at_or(coord.x, y) == TileStatus.EMPTY:
                    grid.set_value_at(coord.x, y, TileStatus.INSIDE)
        if coord.y == last_coord.y:
            # Fill horizontal
            for x in range(min(coord.x, last_coord.x), max(coord.x, last_coord.x) + 1):
                if grid.value_at_or(x, coord.y) == TileStatus.EMPTY:
                    grid.set_value_at(x, coord.y, TileStatus.INSIDE)
        last_coord = coord

    # Fill in the outside
    flood_queue: deque[Coords] = deque()
    for x in range(0, max_x + 3):
        flood_queue.append((Coords(x=x, y=0)))
        flood_queue.append((Coords(x=x, y=max_y + 2)))
    for y in range(0, max_y + 3):
        flood_queue.append((Coords(x=0, y=y)))
        flood_queue.append((Coords(x=max_x + 2, y=y)))

    while len(flood_queue) > 0 and (coord := flood_queue.pop()):
        if grid.value_at_or(coord.x, coord.y, TileStatus.INSIDE) == TileStatus.EMPTY:
            grid.set_value_at(coord.x, coord.y, TileStatus.OUTSIDE)
            for direction in Direction.all():
                new_coord = Coords(*direction.next_coords(coord.x, coord.y))
                if grid.value_at_or(new_coord.x, new_coord.y, TileStatus.INSIDE) == TileStatus.EMPTY:
                    flood_queue.append(new_coord)
    return grid


@register_solver(year="2025", key="9", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    grid = create_grid(puzzle_input)
    grid.print_grid(lambda t: t.str_repr)
    solution = 0
    for y in range(0, grid.height):
        valid_ranges: list[InclusiveRange] = []
        # Make ranges
        last_tile = TileStatus.OUTSIDE
        current_start_x = None
        for x in range(0, grid.width):
            current_tile = grid.value_at_or(x, y, TileStatus.OUTSIDE)
            if current_tile == TileStatus.OUTSIDE and last_tile != TileStatus.OUTSIDE:
                # end a range
                valid_ranges.append(InclusiveRange(start=current_start_x, stop=x-1))
                current_start_x = None
            elif current_tile != TileStatus.OUTSIDE and last_tile == TileStatus.OUTSIDE:
                # start a range
                current_start_x = x
            last_tile = current_tile
        print(f"{valid_ranges=}")
        for valid_range in valid_ranges:
            start_y = y
            end_y = y
            # Determine how much above and below we still have non-OUTSIDE tiles, ie make a solution
            for correction in range(0, grid.height):
                pass
    print(f"Solution is {solution}")
