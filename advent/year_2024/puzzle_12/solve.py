from collections import deque, namedtuple
from collections.abc import Generator
from dataclasses import field, dataclass
from functools import cached_property
from itertools import pairwise, starmap

from advent.registry import register_solver
from advent.utils.enums import PrintEnum, Direction
from advent.utils.grid import Grid


class TileStatus(PrintEnum):
    UNKNOWN = "UNKNOWN", "."
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"
    D = "D", "D"
    E = "E", "E"
    F = "F", "F"
    G = "G", "G"
    H = "H", "H"
    I = "I", "I"
    J = "J", "J"
    K = "K", "K"
    L = "L", "L"
    M = "M", "M"
    N = "N", "N"
    O = "O", "O"
    P = "P", "P"
    Q = "Q", "Q"
    R = "R", "R"
    S = "S", "S"
    T = "T", "T"
    U = "U", "U"
    V = "V", "V"
    W = "W", "W"
    X = "X", "X"
    Y = "Y", "Y"
    Z = "Z", "Z"


TileGrid = Grid[TileStatus]

Coords = namedtuple("Coords", ["x", "y"])


@dataclass
class Region:
    grid: TileGrid
    value: TileStatus
    coords: set[Coords] = field(default_factory=set)

    @property
    def area(self) -> int:
        return len(self.coords)

    @cached_property
    def perimeter(self):
        return sum(
            1 for x, y in self.coords for direction in Direction.all()
            if self.grid.value_at_or(*direction.next_coords(x, y), default=TileStatus.UNKNOWN) != self.value
        )

    @cached_property
    def side_count(self):
        def count_new_side(primary: tuple[int, int], secondary: tuple[int, int]) -> int:
            if primary[0] == secondary[0] and primary[1] + 1 == secondary[1]:
                return 0
            else:
                return 1

        result = 0
        for direction in Direction.all():
            edge_coords: set[Coords] = set()
            for (x, y) in self.coords:
                if self.grid.value_at_or(*direction.next_coords(x, y), default=TileStatus.UNKNOWN) != self.value:
                    edge_coords.add(Coords(x, y))
            if direction in [Direction.WEST, Direction.EAST]:
                extracted_coords = map(lambda c: (c.x, c.y), edge_coords)
            else:
                extracted_coords = map(lambda c: (c.y, c.x), edge_coords)
            result += sum(starmap(count_new_side, pairwise(sorted(extracted_coords)))) + 1
        return result


def generate_regions(grid: TileGrid) -> Generator[Region, None, None]:
    coords_done: set[Coords] = set()
    for x, y, tile in grid.coords_iterator:
        if (x, y) not in coords_done:
            region = Region(grid=grid, value=tile, coords={(x, y)})
            coords: deque[Coords] = deque([Coords(x, y)])
            while coords:
                current_x, current_y = coords.pop()
                for direction in Direction.all():
                    new_x, new_y = direction.next_coords(current_x, current_y)
                    if (new_x, new_y) not in region.coords:
                        if grid.value_at_or(new_x, new_y, default=TileStatus.UNKNOWN) == region.value:
                            coords.append(Coords(new_x, new_y))
                            region.coords.add(Coords(new_x, new_y))
            coords_done.update(region.coords)
            print(f"Defined region for {region.value=} with {region.area=}, {region.perimeter=} and {region.side_count=}")
            yield region


@register_solver(year="2024", key="12", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    print(f"Solution is {sum(map(lambda r: r.area * r.perimeter, generate_regions(grid)))}")


@register_solver(year="2024", key="12", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    print(f"Solution is {sum(map(lambda r: r.area * r.side_count, generate_regions(grid)))}")
