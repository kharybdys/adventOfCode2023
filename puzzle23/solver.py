from collections import deque
from dataclasses import field, dataclass
from typing import Generator, Self

from utils import Grid, PrintEnum, Direction


class TileStatus(PrintEnum):
    PATH = "PATH", "."
    FOREST = "FOREST", "#"
    SLOPE_EAST = "SLOPE_EAST", ">"
    SLOPE_WEST = "SLOPE_WEST", "<"
    SLOPE_NORTH = "SLOPE_NORTH", "^"
    SLOPE_SOUTH = "SLOPE_SOUTH", "v"

    @property
    def can_move_to(self) -> bool:
        return not self == TileStatus.FOREST

    def allowed_exits(self) -> list[Direction]:
        match self:
            case TileStatus.PATH:
                return Direction.all()
            case TileStatus.FOREST:
                return Direction.all()
            case TileStatus.SLOPE_SOUTH:
                return [Direction.SOUTH]
            case TileStatus.SLOPE_NORTH:
                return [Direction.NORTH]
            case TileStatus.SLOPE_EAST:
                return [Direction.EAST]
            case TileStatus.SLOPE_WEST:
                return [Direction.WEST]
            case _:
                raise ValueError(f"Unsupported tile {self}")


TileGrid = Grid[TileStatus]


@dataclass
class Path:
    x: int
    y: int
    visited: set[tuple[int, int]] = field(default_factory=set)

    @property
    def length(self) -> int:
        return len(self.visited)

    def move_to(self, new_x: int, new_y: int) -> Self:
        new_visited = self.visited.copy()
        new_visited.add((self.x, self.y))
        return Path(x=new_x, y=new_y, visited=new_visited)


def find_all_paths(start: Path, grid: TileGrid) -> Generator[Path, None, None]:
    paths = deque()
    paths.append(start)
    while paths:
        path = paths.pop()
        if path.y == grid.height - 1:
            yield path
        for direction in grid.value_at(path.x, path.y).allowed_exits():
            new_x, new_y = direction.next_coords(path.x, path.y)
            if grid.within_bounds(new_x, new_y) and grid.value_at(new_x, new_y).can_move_to and (new_x, new_y) not in path.visited:
                paths.append(path.move_to(new_x, new_y))


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    start_path = Path(0, 0)
    for x in range(0, grid.width):
        if grid.value_at(x, 0).can_move_to:
            start_path = Path(x, 0)
    solution = max(find_all_paths(start_path, grid), key=lambda p: p.length)
    print(f"Found max path with length {solution.length}")


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
