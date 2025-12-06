import sys
from collections import deque, namedtuple
from copy import deepcopy
from typing import Generic, Self, Callable, Generator, TypeVar

from advent.utils.enums import Direction

T = TypeVar("T")


class Grid(Generic[T]):
    def __init__(self, tiles: list[list[T]]):
        self.tiles: list[list[T]] = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])

    def copy(self) -> Self:
        return self.__class__(deepcopy(self.tiles))

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

    def all_coords_for(self, values: set[T]) -> Generator[tuple[int, int], None, None]:
        for x, y, tile in self.coords_iterator:
            if tile in values:
                yield x, y


Coords = namedtuple("Coords", ["x", "y"])


def shortest_path_analysis(grid: Grid[T], start_tile: T, wall_tile: T) -> dict[Coords, int]:
    visited: dict[Coords, int] = {}
    for start_coords in grid.all_coords_for({start_tile}):
        visited[start_coords] = 0
    boundary: deque[Coords] = deque()
    boundary.extend(grid.all_coords_for({start_tile}))
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
