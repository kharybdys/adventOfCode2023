from collections import defaultdict
from collections.abc import Generator
from itertools import combinations

from advent.year_2024.puzzle_8.tile import TileGrid, TileStatus
from advent.registry import register_solver
from advent.utils.grid import Grid


def analyze(grid: TileGrid) -> dict[TileStatus, list[tuple[int, int]]]:
    result: dict[TileStatus, list[tuple[int, int]]] = defaultdict(list)
    for x, y, tile in grid.coords_iterator:
        if tile != TileStatus.EMPTY:
            result[tile].append((x, y))
    return result


def calculate_antinodes(coords: list[tuple[int, int]]) -> Generator[tuple[int, int], None, None]:
    for (x, y), (other_x, other_y) in combinations(coords, 2):
        diff_x = other_x - x
        diff_y = other_y - y
        yield x - diff_x, y - diff_y
        yield other_x + diff_x, other_y + diff_y


def calculate_antinodes_infinite(grid: TileGrid, coords: list[tuple[int, int]]) -> Generator[tuple[int, int], None, None]:
    print(f"Calculating anti_nodes for given coords: {coords}")
    for (x, y), (other_x, other_y) in combinations(coords, 2):
        print(f"Calculating anti_nodes for ({x}, {y}) and ({other_x}, {other_y})")
        diff_x = other_x - x
        diff_y = other_y - y
        # Prime candidate for extraction for violation DRY
        multiplier = 0
        while grid.within_bounds(x - multiplier * diff_x, y - multiplier * diff_y):
            print(f"Yielding ({x - multiplier * diff_x}, {y - multiplier * diff_y}) for multiplier {multiplier} in the negative direction")
            yield x - multiplier * diff_x, y - multiplier * diff_y
            multiplier += 1
        multiplier = 0
        while grid.within_bounds(other_x + multiplier * diff_x, other_y + multiplier * diff_y):
            print(f"Yielding ({other_x + multiplier * diff_x}, {other_y + multiplier * diff_y}) for multiplier {multiplier} in the positive direction")
            yield other_x + multiplier * diff_x, other_y + multiplier * diff_y
            multiplier += 1


@register_solver(year="2024", key="8", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    analyzed_grid = analyze(grid)
    anti_nodes: set[tuple[int, int]] = set()
    for coords in analyzed_grid.values():
        anti_nodes.update(calculate_antinodes(coords))
    solution = len([anti_node for anti_node in anti_nodes if grid.within_bounds(*anti_node)])
    print_grid_and_anti_nodes(grid, anti_nodes)
    print(f"Solution is {solution}")


def print_grid_and_anti_nodes(grid: TileGrid, anti_nodes: set[tuple[int, int]]):
    def print_function(coords: set[tuple[int, int]], x: int, y: int, tile: TileStatus) -> str:
        if tile != TileStatus.EMPTY:
            return tile.str_repr
        elif (x, y) in coords:
            return "#"
        else:
            return TileStatus.EMPTY.str_repr

    for row in range(0, grid.height):
        print("".join(print_function(anti_nodes, column, row, tile) for column, tile in enumerate(grid.tiles[row])))


@register_solver(year="2024", key="8", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    analyzed_grid = analyze(grid)
    anti_nodes: set[tuple[int, int]] = set()
    for coords in analyzed_grid.values():
        anti_nodes.update(calculate_antinodes_infinite(grid, coords))

    print_grid_and_anti_nodes(grid, anti_nodes)
    print(f"Solution is {len(anti_nodes)}")
