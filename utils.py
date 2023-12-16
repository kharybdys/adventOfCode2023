from enum import Enum
from functools import cached_property
from itertools import groupby
from typing import Generator, Self


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def split_in_groups_separated_by_empty_line(puzzle_input: list[str]) -> Generator[list[str], None, None]:
    lines = []
    for line in puzzle_input:
        if line:
            lines.append(line)
        else:
            yield lines
            lines = []
    yield lines


class Direction(Enum):
    EAST = "EAST", "<"
    WEST = "WEST", ">"
    SOUTH = "SOUTH", "^"
    NORTH = "NORTH", "v"

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    def next_coords(self, x: int, y: int) -> tuple[int, int]:
        match self:
            case Direction.EAST:
                return x + 1, y
            case Direction.WEST:
                return x - 1, y
            case Direction.NORTH:
                return x, y - 1
            case Direction.SOUTH:
                return x, y + 1
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @cached_property
    def opposite(self) -> Self:
        match self:
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @classmethod
    def all(cls) -> list[Self]:
        return list(cls.__members__.values())
