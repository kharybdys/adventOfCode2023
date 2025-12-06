from collections import namedtuple, defaultdict
from copy import copy
from dataclasses import dataclass, field
from functools import partial
from queue import PriorityQueue

from advent.registry import register_solver
from advent.utils.enums import PrintEnum, Direction
from advent.utils.grid import Grid


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    WALL = "WALL", "#"
    START = "START", "S"
    END = "END", "E"


TileGrid = Grid[TileStatus]

Coords = namedtuple("Coords", ["x", "y"])


@dataclass(order=True, unsafe_hash=True)
class Visit:
    cost: int
    coords: Coords = field(compare=False)
    direction: Direction = field(compare=False)
    already_visited: set[Coords] = field(default_factory=set, compare=False, repr=False)


def find_start_coords(grid: TileGrid) -> Coords:
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.START:
            return Coords(x, y)
    raise ValueError("Grid does not contain a START position")


def merge_discard_or_keep(visit: Visit, visitations: dict[Coords, list[Visit]]) -> Visit | None:
    for other_visit in visitations[visit.coords]:
        if other_visit.direction == visit.direction:
            if other_visit.cost == visit.cost:
                other_visit.already_visited.update(visit.already_visited)
            else:
                # discard
                return None
    visitations[visit.coords].append(visit)
    return visit


def analyze_grid(grid: TileGrid) -> dict[Coords, list[Visit]]:
    result: dict[Coords, list[Visit]] = defaultdict(list)
    to_check: PriorityQueue[Visit] = PriorityQueue()
    to_check.put(
        Visit(
            coords=find_start_coords(grid),
            direction=Direction.EAST,
            cost=0,
        )
    )
    while not to_check.empty():
        visit = to_check.get_nowait()
        for direction in visit.direction.opposite.all_but_me:
            if grid.value_at_or(*direction.next_coords(*visit.coords), default=TileStatus.WALL) != TileStatus.WALL:
                extra_cost = 1
                if direction != visit.direction:
                    extra_cost += 1000
                new_already_visited = copy(visit.already_visited)
                new_already_visited.add(visit.coords)
                new_visit = Visit(
                    coords=Coords(*direction.next_coords(*visit.coords)),
                    direction=direction,
                    cost=visit.cost + extra_cost,
                    already_visited=new_already_visited,
                )
                if keep_visit := merge_discard_or_keep(new_visit, result):
                    to_check.put(keep_visit)
    return result


@register_solver(year="2024", key="16", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    fastest_to = analyze_grid(grid)
    for coords, visits in fastest_to.items():
        if grid.value_at(*coords) == TileStatus.END:
            distance = min(visit.cost for visit in visits)
            print(f"Solution is {distance}")


def print_function(x: int, y: int, tile: TileStatus, coords_visited: set[Coords]) -> str:
    if Coords(x, y) in coords_visited:
        return "O"
    else:
        return tile.str_repr


@register_solver(year="2024", key="16", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    fastest_to = analyze_grid(grid)
    for coords, visits in fastest_to.items():
        if grid.value_at(*coords) == TileStatus.END:
            distance = min(visit.cost for visit in visits)
            coords_visited = set()
            for visit in visits:
                if visit.cost == distance:
                    coords_visited.update(visit.already_visited)
            if example:
                grid.print_grid_using_coords(partial(print_function, coords_visited=coords_visited))
            print(f"Solution is {len(coords_visited) + 1}")
