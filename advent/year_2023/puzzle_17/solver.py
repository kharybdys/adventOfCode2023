from dataclasses import dataclass, field, replace
from functools import cached_property, cache
from queue import PriorityQueue
from typing import Self

from registry import register_solver
from utils import Direction, Grid

IntGrid = Grid[int]


@cache
def calculate_remaining_distance(grid: IntGrid) -> dict[tuple[int, int], int]:
    # TODO: Quite probably this is not a correct minimum distance in some situations - but doesn't solve it
    result: dict[tuple[int, int], int] = {(grid.width - 1, grid.height - 1): 0}
    max_summed_coords = grid.width + grid.height - 2
    for diff_summed_coords in range(1, max_summed_coords + 1):
        for x_coord in range(max(0, grid.width - diff_summed_coords - 1), min(grid.width, max_summed_coords - diff_summed_coords + 1)):
            y_coord = max_summed_coords - diff_summed_coords - x_coord
            next_coords: list[tuple[int, int]] = [direction.next_coords(x_coord, y_coord) for direction in [Direction.SOUTH, Direction.EAST]]
            result[(x_coord, y_coord)] = min(result[new_x, new_y] + grid.value_at(new_x, new_y)
                                             for new_x, new_y in next_coords
                                             if grid.within_bounds(new_x, new_y))
    return result


@dataclass(repr=True)
class Attempt:
    cost: int
    x: int
    y: int
    end_x: int
    end_y: int
    entry: Direction
    straight_steps_taken: int
    grid: IntGrid
    route: dict[tuple[int, int], Direction] = field(default_factory=dict)

    @cached_property
    def minimal_cost(self) -> int:
        remaining_distances = calculate_remaining_distance(self.grid)
        return self.cost + remaining_distances[(self.x, self.y)]

    @cached_property
    def primary_key(self) -> tuple[int, int, Direction, int]:
        return self.x, self.y, self.entry, self.straight_steps_taken

    def at_finish(self) -> bool:
        return self.x == self.end_x and self.y == self.end_y

    def next_attempt(self, new_x: int, new_y: int, cost_addition: int, new_entry: Direction) -> Self:
        new_straight_steps_taken = 1 if new_entry != self.entry else self.straight_steps_taken + 1
        new_route = self.route.copy()
        new_route[(self.x, self.y)] = self.entry
        return replace(self,
                       cost=self.cost + cost_addition,
                       x=new_x,
                       y=new_y,
                       entry=new_entry,
                       route=new_route,
                       straight_steps_taken=new_straight_steps_taken)

    def __lt__(self, other) -> bool:
        if isinstance(other, Attempt):
            return self.minimal_cost < other.minimal_cost
        else:
            raise TypeError(f"Cannot compare {self} with {other}")


def print_route_and_grid(route: dict[tuple[int, int], Direction], grid: IntGrid):
    for y in range(0, grid.height):
        print("".join(route[(x, y)].str_repr if (x, y) in route else str(grid.value_at(x, y)) for x in range(0, grid.width)))


def find_minimal_path(grid: IntGrid, first_attempts: list[Attempt], min_straight_steps: int, max_straight_steps: int) -> int:
    UPPER_LIMIT = 1000000000
    print(f"Starting with {first_attempts=}")
    already_tried_attempts: dict[tuple[int, int, Direction, int], int] = {}
    attempts = PriorityQueue()
    for first_attempt in first_attempts:
        attempts.put_nowait(first_attempt)
    best_cost = UPPER_LIMIT
    while not attempts.empty():
        attempt: Attempt = attempts.get_nowait()
        # print(f"Looking at {attempt.minimal_cost}")

        if attempt.at_finish():
            # With correct remaining distance, ending here should be enough
            print_route_and_grid(attempt.route, grid)
            if attempt.cost < best_cost:
                best_cost = attempt.cost
                print(f"Improved best_cost to {attempt.cost}")
        elif attempt.cost < best_cost:
            already_tried_attempts[attempt.primary_key] = min(already_tried_attempts.get(attempt.primary_key, UPPER_LIMIT), attempt.cost)
            for direction in attempt.entry.all_but_me:
                straight_acceptable = direction == attempt.entry.opposite and attempt.straight_steps_taken < max_straight_steps
                turn_acceptable = direction not in (attempt.entry, attempt.entry.opposite) and attempt.straight_steps_taken >= min_straight_steps
                if straight_acceptable or turn_acceptable:
                    new_x, new_y = direction.next_coords(attempt.x, attempt.y)
                    if grid.within_bounds(new_x, new_y):
                        next_attempt = attempt.next_attempt(new_x, new_y, grid.value_at(new_x, new_y), direction.opposite)
                        if next_attempt.cost < already_tried_attempts.get(next_attempt.primary_key, UPPER_LIMIT):
                          attempts.put_nowait(next_attempt)
    return best_cost


@register_solver(year="2023", key="17", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid = Grid.from_lines(puzzle_input, int)
    first_attempt = Attempt(cost=0,
                            x=0,
                            y=0,
                            end_x=grid.width - 1,
                            end_y=grid.height - 1,
                            entry=Direction.NORTH,
                            straight_steps_taken=0,
                            grid=grid
                            )
    print(find_minimal_path(grid=grid,
                            first_attempts=[first_attempt, replace(first_attempt, entry=Direction.WEST)],
                            min_straight_steps=0,
                            max_straight_steps=3))


@register_solver(year="2023", key="17", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid = Grid.from_lines(puzzle_input, int)
    first_attempt = Attempt(cost=0,
                            x=0,
                            y=0,
                            end_x=grid.width - 1,
                            end_y=grid.height - 1,
                            entry=Direction.NORTH,
                            straight_steps_taken=0,
                            grid=grid
                            )
    print(find_minimal_path(grid=grid,
                            first_attempts=[first_attempt, replace(first_attempt, entry=Direction.WEST)],
                            min_straight_steps=4,
                            max_straight_steps=10))
