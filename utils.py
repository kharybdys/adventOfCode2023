import sys
from collections import namedtuple, deque
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from itertools import groupby
from typing import Generator, Self, TypeVar, Generic, Callable, Protocol


class SolverFunction(Protocol):
    def __call__(self,
                 puzzle_input: list[str],
                 example: bool) -> None:
        pass


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


Coords = namedtuple("Coords", ["x", "y"])


@dataclass
class Range:
    start: int
    stop: int

    @cached_property
    def size(self) -> int:
        return self.stop - self.start

    def within(self, value: float) -> bool:
        return self.start <= value < self.stop

    def before(self, value: float | int) -> bool:
        return self.stop <= value

    def after(self, value: float | int) -> bool:
        return self.start > value


@dataclass
class InclusiveRange(Range):
    @cached_property
    def size(self) -> int:
        return self.stop - self.start + 1

    def within(self, value: float | int) -> bool:
        return self.start <= value <= self.stop


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


T = TypeVar("T")


class Grid(Generic[T]):
    def __init__(self, tiles: list[list[T]]):
        self.tiles: list[list[T]] = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])

    @staticmethod
    def from_size(width: int, height: int, tile: T) -> Self:
        return Grid(tiles=[[tile for _ in range(width)] for _ in range(height)])

    @staticmethod
    def from_lines(lines: list[str], converter_function: Callable[[str], T]) -> Self:
        return Grid(tiles=[[converter_function(char) for char in line] for line in lines])

    def within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def value_at(self, x: int, y: int) -> T:
        return self.tiles[y][x]

    def value_at_or(self, x: int, y: int, default: T | None = None) -> T | None:
        if self.within_bounds(x, y):
            return self.tiles[y][x]
        else:
            return default

    def set_value_at(self, x: int, y: int, value: T):
        if self.within_bounds(x, y):
            self.tiles[y][x] = value
        else:
            raise KeyError(f"Invalid coordinates {x}, {y} for grid with width {self.width} and height {self.height}")

    @property
    def coords_iterator(self) -> Generator[tuple[int, int, T], None, None]:
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield x, y, self.value_at(x, y)

    @property
    def tiles_iterator(self) -> Generator[T, None, None]:
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield self.value_at(x, y)

    def print_grid(self, print_function: Callable[[T], str]):
        for y in range(0, self.height):
            print("".join(print_function(tile) for tile in self.tiles[y]))

    def print_grid_using_coords(self, print_function: Callable[[int, int, T], str]):
        for y in range(0, self.height):
            print("".join(print_function(x, y, tile) for x, tile in enumerate(self.tiles[y])))

    def all_coords_for(self, value: T) -> Generator[tuple[int, int], None, None]:
        for x, y, tile in self.coords_iterator:
            if tile == value:
                yield x, y


def shortest_path_analysis(grid: Grid[T], start_tile: T, wall_tile: T) -> dict[Coords, int]:
    visited: dict[Coords, int] = {}
    for start_coords in grid.all_coords_for(start_tile):
        visited[start_coords] = 0
    boundary: deque[Coords] = deque()
    boundary.extend(grid.all_coords_for(start_tile))
    while boundary:
        coords = boundary.pop()
        for direction in Direction.all():
            new_coords = direction.next_coords(*coords)
            if grid.value_at_or(*new_coords, default=wall_tile) != wall_tile:
                old_visit = visited.get(new_coords, sys.maxsize)
                if old_visit > visited[coords] + 1:
                    visited[new_coords] = visited[coords] + 1
                    boundary.append(new_coords)
    return visited
