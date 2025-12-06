import re
import sys
from collections import deque
from collections.abc import Generator

from registry import register_solver
from advent.utils.enums import PrintEnum, Direction
from advent.utils.grid import Grid, Coords


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    WALL = "WALL", "#"


TileGrid = Grid[TileStatus]


def parse_bits(puzzle_input: list[str]) -> Generator[Coords, None, None]:
    BIT_PATTERN = re.compile(r"(?P<x>\d+),(?P<y>\d+)")
    for line in puzzle_input:
        if line_match := BIT_PATTERN.fullmatch(line):
            yield Coords(int(line_match.group("x")), int(line_match.group("y")))
        else:
            raise ValueError(f"Cannot parse line {line}")


def drop_bits(grid: TileGrid, bits: list[Coords]):
    for bit in bits:
        grid.set_value_at(*bit, value=TileStatus.WALL)


def length_shortest_path(grid: TileGrid, start_coords: Coords, end_coords: Coords) -> int:
    visited: dict[Coords, int] = {start_coords: 0}
    boundary: deque[Coords] = deque()
    boundary.append(start_coords)
    while boundary:
        coords = boundary.pop()
        for direction in Direction.all():
            new_coords = direction.next_coords(*coords)
            if grid.value_at_or(*new_coords, default=TileStatus.WALL) != TileStatus.WALL:
                old_visit = visited.get(new_coords, sys.maxsize)
                if old_visit > visited[coords] + 1:
                    visited[new_coords] = visited[coords] + 1
                    boundary.append(new_coords)
    return visited[end_coords]


@register_solver(year="2024", key="18", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    size = 7 if example else 71
    start_coords = Coords(0, 0)
    end_coords = Coords(size - 1, size - 1)

    grid = Grid.from_size(size, size, TileStatus.EMPTY)
    bits = list(parse_bits(puzzle_input))

    drop_bits(grid, bits[:12 if example else 1024])

    solution = length_shortest_path(grid, start_coords, end_coords)
    print(f"Solution is {solution}")


def reachable(grid: TileGrid, start_coords: Coords, end_coords: Coords) -> bool:
    visited: set[Coords] = set()
    newly_visited: set[Coords] = {start_coords}
    while newly_visited and end_coords not in newly_visited:
        visited.update(newly_visited)
        newly_visited = {direction.next_coords(*old_coords)
                         for direction in Direction.all()
                         for old_coords in newly_visited
                         if grid.value_at_or(*direction.next_coords(*old_coords), default=TileStatus.WALL) != TileStatus.WALL
                         }
        newly_visited.difference_update(visited)
    return end_coords in newly_visited


def determine_first_blocking_bit(grid: TileGrid, bits: list[Coords], start_coords: Coords, end_coords: Coords):
    index = 0
    while reachable(grid, start_coords, end_coords):
        grid.set_value_at(*bits[index], value=TileStatus.WALL)
        index += 1
    return bits[index - 1]


@register_solver(year="2024", key="18", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    size = 7 if example else 71
    start_coords = Coords(0, 0)
    end_coords = Coords(size - 1, size - 1)

    grid = Grid.from_size(size, size, TileStatus.EMPTY)
    bits = list(parse_bits(puzzle_input))

    print(f"Solution is {determine_first_blocking_bit(grid, bits, start_coords, end_coords)}")
