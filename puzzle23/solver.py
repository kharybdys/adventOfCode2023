from utils import Grid, PrintEnum


class TileStatus(PrintEnum):
    PATH = "PATH", "."
    FOREST = "FOREST", "#"
    SLOPE_EAST = "SLOPE_EAST", ">"
    SLOPE_WEST = "SLOPE_WEST", "<"
    SLOPE_NORTH = "SLOPE_NORTH", "^"
    SLOPE_SOUTH = "SLOPE_SOUTH", "v"


TileGrid = Grid[TileStatus]


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
