from collections import namedtuple
from enum import Enum
from typing import Self

from utils import Grid, Direction


class TileStatus(Enum):
    EMPTY = "EMPTY", "."
    ROCK = "ROCK", "#"
    START = "START", "S"

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    def __bool__(self) -> bool:
        return self == TileStatus.ROCK

    @classmethod
    def from_char(cls, char: str) -> Self:
        for opt in cls.__members__.values():
            if opt.str_repr == char:
                return opt
        raise ValueError(f"Unknown char {char}")


TileGrid = Grid[TileStatus]

Coords = namedtuple("Coords", ["x", "y"])


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    coords: set = set()
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.START:
            coords.add(Coords(x, y))
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


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
