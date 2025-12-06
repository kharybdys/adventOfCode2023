from enum import Enum
from functools import cached_property
from typing import Self


class PrintEnum(Enum):
    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    @classmethod
    def from_char(cls, char: str) -> Self:
        for opt in cls.__members__.values():
            if opt.str_repr == char:
                return opt
        raise ValueError(f"Unknown char {char}")


class Direction(PrintEnum):
    EAST = "EAST", "<"
    WEST = "WEST", ">"
    SOUTH = "SOUTH", "^"
    NORTH = "NORTH", "v"

    def __new__(cls, value, str_repr):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_repr = str_repr
        return obj

    def __lt__(self, other) -> bool:
        if isinstance(other, Direction):
            return self.value < other.value
        else:
            raise TypeError(f"Cannot compare {self} with {other}")

    def next_coords(self, x: int, y: int, steps: int = 1) -> tuple[int, int]:
        match self:
            case Direction.EAST:
                return x + steps, y
            case Direction.WEST:
                return x - steps, y
            case Direction.NORTH:
                return x, y - steps
            case Direction.SOUTH:
                return x, y + steps
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @property
    def horizontal(self) -> bool:
        return self in [Direction.EAST, Direction.WEST]

    @property
    def vertical(self) -> bool:
        return self in [Direction.NORTH, Direction.SOUTH]

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

    @cached_property
    def cw(self) -> Self:
        match self:
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH
            case Direction.NORTH:
                return Direction.EAST
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @cached_property
    def ccw(self) -> Self:
        match self:
            case Direction.EAST:
                return Direction.NORTH
            case Direction.NORTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.EAST
            case _:
                raise ValueError(f"Impossible, unsupported direction: {self}")

    @cached_property
    def all_but_me(self) -> list[Self]:
        result = self.all()
        result.remove(self)
        return result

    @classmethod
    def all(cls) -> list[Self]:
        return list(cls.__members__.values())
