from advent.registry import register_solver
from advent.utils.enums import PrintEnum
from advent.utils.grid import Grid


class TileStatus(PrintEnum):
    X = "X", "X"
    M = "M", "M"
    A = "A", "A"
    S = "S", "S"


TileGrid = Grid[TileStatus]


def count_xmas(grid: TileGrid) -> int:
    result = 0
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.X:
            # E
            if grid.value_at_or(x + 1, y) == TileStatus.M:
                if grid.value_at_or(x + 2, y) == TileStatus.A and grid.value_at_or(x + 3, y) == TileStatus.S:
                    result += 1
            # SE
            if grid.value_at_or(x + 1, y + 1) == TileStatus.M:
                if grid.value_at_or(x + 2, y + 2) == TileStatus.A and grid.value_at_or(x + 3, y + 3) == TileStatus.S:
                    result += 1
            # S
            if grid.value_at_or(x, y + 1) == TileStatus.M:
                if grid.value_at_or(x, y + 2) == TileStatus.A and grid.value_at_or(x, y + 3) == TileStatus.S:
                    result += 1
            # SW
            if grid.value_at_or(x - 1, y + 1) == TileStatus.M:
                if grid.value_at_or(x - 2, y + 2) == TileStatus.A and grid.value_at_or(x - 3, y + 3) == TileStatus.S:
                    result += 1
            # W
            if grid.value_at_or(x - 1, y) == TileStatus.M:
                if grid.value_at_or(x - 2, y) == TileStatus.A and grid.value_at_or(x - 3, y) == TileStatus.S:
                    result += 1
            # NW
            if grid.value_at_or(x - 1, y - 1) == TileStatus.M:
                if grid.value_at_or(x - 2, y - 2) == TileStatus.A and grid.value_at_or(x - 3, y - 3) == TileStatus.S:
                    result += 1
            # N
            if grid.value_at_or(x, y - 1) == TileStatus.M:
                if grid.value_at_or(x, y - 2) == TileStatus.A and grid.value_at_or(x, y - 3) == TileStatus.S:
                    result += 1
            # NE
            if grid.value_at_or(x + 1, y - 1) == TileStatus.M:
                if grid.value_at_or(x + 2, y - 2) == TileStatus.A and grid.value_at_or(x + 3, y - 3) == TileStatus.S:
                    result += 1
    return result


def count_x_mas(grid: TileGrid) -> int:
    result = 0
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.A:
            # S
            if grid.value_at_or(x + 1, y + 1) == TileStatus.M and grid.value_at_or(x - 1, y + 1) == TileStatus.M:
                if grid.value_at_or(x - 1, y - 1) == TileStatus.S and grid.value_at_or(x + 1, y - 1) == TileStatus.S:
                    result += 1
            # W
            if grid.value_at_or(x - 1, y + 1) == TileStatus.M and grid.value_at_or(x - 1, y - 1) == TileStatus.M:
                if grid.value_at_or(x + 1, y - 1) == TileStatus.S and grid.value_at_or(x + 1, y + 1) == TileStatus.S:
                    result += 1
            # N
            if grid.value_at_or(x - 1, y - 1) == TileStatus.M and grid.value_at_or(x + 1, y - 1) == TileStatus.M:
                if grid.value_at_or(x + 1, y + 1) == TileStatus.S and grid.value_at_or(x - 1, y + 1) == TileStatus.S:
                    result += 1
            # E
            if grid.value_at_or(x + 1, y - 1) == TileStatus.M and grid.value_at_or(x + 1, y + 1) == TileStatus.M:
                if grid.value_at_or(x - 1, y + 1) == TileStatus.S and grid.value_at_or(x - 1, y - 1) == TileStatus.S:
                    result += 1
    return result


@register_solver(year="2024", key="4", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    print(f"Solution is {count_xmas(grid)}")


@register_solver(year="2024", key="4", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    print(f"Solution is {count_x_mas(grid)}")
