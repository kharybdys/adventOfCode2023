from collections import deque
from collections.abc import Generator
from dataclasses import dataclass, field
from itertools import starmap
from typing import Self

from advent.registry import register_solver
from advent.utils.enums import PrintEnum, Direction
from advent.utils.grid import Grid, Coords


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    CHAIR = "CHAIR", "o"
    GOAL_CHAIR = "GOAL_CHAIR", "O"


TileGrid = Grid[TileStatus]


@dataclass
class Attempt:
    grid: TileGrid
    moves: list[tuple[Coords, Direction]] = field(default_factory=list)

    def next_attempt(self, coords: Coords, direction: Direction) -> Self | None:
        grid = self.grid.copy()
        chair_to_move = grid.value_at(*coords)
        if chair_to_move == TileStatus.EMPTY:
            raise ValueError("Cannot move empty space")
        if coords.x in [0, grid.width - 1] or coords.y in [0, grid.height - 1]:
            raise ValueError("Cannot move something on the edge")

        grid.set_value_at(*coords, value=TileStatus.EMPTY)
        last_coords = coords
        while grid.value_at_or(*last_coords, default=TileStatus.CHAIR) == TileStatus.EMPTY:
            last_coords = Coords(*direction.next_coords(*last_coords))
        grid.set_value_at(*direction.opposite.next_coords(*last_coords), value=chair_to_move)

        new_moves = self.moves.copy()
        new_moves.append((coords, direction))
        return self.__class__(grid=grid, moves=new_moves)

    @property
    def primary_key(self) -> tuple[Coords, ...]:
        chair_coords = list(starmap(Coords, self.grid.all_coords_for({TileStatus.CHAIR})))
        goal_chair_coords = list(starmap(Coords, self.grid.all_coords_for({TileStatus.GOAL_CHAIR})))
        return tuple(sorted(chair_coords) + sorted(goal_chair_coords))

    @property
    def finished(self) -> bool:
        if self.grid.value_at(self.grid.width // 2, self.grid.height // 2) == TileStatus.GOAL_CHAIR:
            return True
        else:
            return False

    @property
    def unfinishable(self) -> bool:
        goal_chair_coords = list(self.grid.all_coords_for({TileStatus.GOAL_CHAIR}))
        if len(goal_chair_coords) != 1:
            raise ValueError("Got multiple goal chairs on the grid, huh?")
        x, y = goal_chair_coords[0]
        return x in [0, self.grid.width - 1] or y in [0, self.grid.height - 1]


def generate_possible_moves(grid: TileGrid) -> Generator[tuple[Coords, Direction]]:
    for x, y in grid.all_coords_for({TileStatus.CHAIR, TileStatus.GOAL_CHAIR}):
        # Ignore chairs on the edge of the grid (they're off the tables)
        if x not in [0, grid.width - 1]:
            if y not in [0, grid.height - 1]:
                for direction in Direction.all():
                    if grid.value_at(*direction.next_coords(x, y)) == TileStatus.EMPTY:
                        yield Coords(x, y), direction


@register_solver(year="vierkant", key="sokoban", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    grid = Grid.from_lines(puzzle_input, TileStatus.from_char)

    visited: set[tuple[Coords, ...]] = set()

    attempts: deque[Attempt] = deque()
    attempts.append(Attempt(grid))
    while attempts:
        print(f"Considering {len(attempts)} attempts, visited: {len(visited)}")
        # Breadth first
        attempt = attempts.popleft()
        if attempt.finished:
            print(f"Solution: {attempt.moves}")
            return
        if attempt.primary_key in visited:
            continue
        visited.add(attempt.primary_key)
        if attempt.unfinishable:
            continue
        for coords, direction in generate_possible_moves(attempt.grid):
            next_attempt = attempt.next_attempt(coords, direction)
            if next_attempt is not None and next_attempt.primary_key not in visited:
                attempts.append(next_attempt)
