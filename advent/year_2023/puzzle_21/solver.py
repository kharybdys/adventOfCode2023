import pprint
from collections import namedtuple, defaultdict
from dataclasses import dataclass
from typing import Generator

from registry import register_solver
from utils import Grid, Direction, PrintEnum


class TileStatus(PrintEnum):
    EMPTY = "EMPTY", "."
    ROCK = "ROCK", "#"
    START = "START", "S"

    def __bool__(self) -> bool:
        return self == TileStatus.ROCK


TileGrid = Grid[TileStatus]

Coords = namedtuple("Coords", ["x", "y"])


def get_start_coord(grid: TileGrid) -> tuple[int, int]:
    for x, y, tile in grid.coords_iterator:
        if tile == TileStatus.START:
            return x, y


@register_solver(year="2023", key="21", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    coords: set = set()
    coords.add(Coords(*get_start_coord(grid)))
    for step in range(0, 64):
        print(f"Beginning of {step=}, total coords: {len(coords)}")
        new_coords = set()
        for coord in coords:
            for direction in Direction.all():
                new_coord = Coords(*direction.next_coords(coord.x, coord.y))
                if grid.within_bounds(*new_coord) and not grid.value_at(*new_coord):
                    new_coords.add(new_coord)
        coords = new_coords
    print(len(coords))


def grid_value_at_wrapped(x: int, y: int, grid: TileGrid) -> TileStatus:
    lim_x = x % grid.width
    lim_y = y % grid.height
    return grid.value_at(lim_x, lim_y)


def generate_coordinates(step: int) -> Generator[tuple[int, int], None, None]:
    for current_sum in range(-step, step + 1, 2):
        if current_sum > 0:
            for x in range(0, step + 1):
                y = current_sum - x
                yield x, y
        elif current_sum < 0:
            for x in range(-step, 1):
                y = current_sum - x
                yield x, y
        else:
            half_step = step // 2
            for x in range(-half_step, half_step + 1):
                y = current_sum - x
                yield x, y


def calculate_valid_targets(start_x: int, start_y: int, grid: TileGrid, step: int) -> int:
    solution = 0
    for x, y in generate_coordinates(step):
        # print(f"Checking  {x}, {y}")
        if grid_value_at_wrapped(x=x + start_x, y=y + start_y, grid=grid) != TileStatus.ROCK:
            # print(f"Not a rock at {x + start_x}, {y + start_y}.")
            solution += 1
    return solution


def solve_b_too_high(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    steps_to_check = [6, 10, 50, 100, 500, 1000, 5000] if example else [26501365]
    # Need to check target_step * target_step options, centered on start_x, start_y
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    start_x, start_y = get_start_coord(grid)
    # Approach might still be too slow
    # More importantly, counting too many since some squares will not have been reachable due to a rock on an earlier step
    for step in steps_to_check:
        print(f"{step=}: {calculate_valid_targets(start_x, start_y, grid, step=step + 1)}")


DEBUG = False


@dataclass
class CoordsMapping:
    target: Coords
    offset: Coords


def wrap_coords(x: int, y: int, grid: TileGrid) -> tuple[int, int, int, int]:
    lim_x = x % grid.width
    lim_y = y % grid.height
    return lim_x, lim_y, x - lim_x, y - lim_y


def generate_coords_mapping_for_step_size(step_size: int, grid: TileGrid) -> dict[Coords, dict[Coords, set[Coords]]]:
    result: dict[Coords, dict[Coords, set[Coords]]] = {}
    # Generate a mapping for one step
    coords_mapping: dict[Coords, list[CoordsMapping]] = defaultdict(list)
    for x, y, tile in grid.coords_iterator:
        if not tile:
            for direction in Direction.all():
                new_x, new_y, offset_x, offset_y = wrap_coords(*direction.next_coords(x, y), grid=grid)
                if not grid.value_at_or(new_x, new_y):
                    coords_mapping[Coords(x, y)].append(CoordsMapping(Coords(new_x, new_y), Coords(offset_x, offset_y)))
    # For each "starting coordinate", generate the step_sized mapping
    for x, y, tile in grid.coords_iterator:
        if not tile:
            coords_offsets: dict[Coords, set[Coords]] = defaultdict(set)
            coords_offsets[Coords(x, y)].add(Coords(0, 0))
            for step in range(step_size):
                new_coords_offsets: dict[Coords, set[Coords]] = defaultdict(set)
                for coords, offsets in coords_offsets.items():
                    for new_coords_mapping in coords_mapping.get(coords, []):
                        new_offsets: set[Coords] = {Coords(x=offset.x + new_coords_mapping.offset.x,
                                                           y=offset.y + new_coords_mapping.offset.y) for offset in offsets}
                        new_coords_offsets[new_coords_mapping.target].update(new_offsets)
                coords_offsets = new_coords_offsets
            result[Coords(x, y)] = coords_offsets
    return result


@register_solver(year="2023", key="21", variation="b")
def solve_b_too_slow(puzzle_input: list[str], example: bool) -> None:
    print("\n".join(puzzle_input))
    # 26501365 = 5 * 11 * 481843
    # 26501365 = 5146^2 + 20049
    # 20049 = 3 * 41 * 163
    # 5146 = 2 * 31 * 83
    steps_to_check = [10, 50, 100, 500, 1000, 5000] if example else [26501365]
    grid: TileGrid = Grid.from_lines(puzzle_input, TileStatus.from_char)
    start_x, start_y = get_start_coord(grid)

    step_size = 10 if example else 55  # These are factors of the steps_to_check values

    coords_mapping: dict[Coords, dict[Coords, set[Coords]]] = generate_coords_mapping_for_step_size(step_size, grid)
    print(f"Mapping: {pprint.pprint(coords_mapping)}")

    # list[Coords] is the list of offsets in which this coordinate pair is reachable
    coords_offsets: dict[Coords, set[Coords]] = defaultdict(set)
    coords_offsets[Coords(start_x, start_y)].add(Coords(0, 0))

    for step in range(step_size, steps_to_check[-1] + 1, step_size):
        new_coords_offsets: dict[Coords, set[Coords]] = defaultdict(set)
        for coords, offsets in coords_offsets.items():
            if DEBUG:
                print(f"Adding new_coords: {coords_mapping.get(coords, [])} for {coords}")
            for new_coords, new_offsets in coords_mapping.get(coords, {}).items():
                combined_offsets: set[Coords] = {Coords(x=offset.x + new_offset.x,
                                                        y=offset.y + new_offset.y) for offset in offsets for new_offset in new_offsets}
                new_coords_offsets[new_coords].update(combined_offsets)
        coords_offsets = new_coords_offsets

        if step in steps_to_check:
            print(f"At step {step}, solution is {sum(map(len, coords_offsets.values()))}")
            if DEBUG:
                print(f"Counter: {pprint.pprint(coords_offsets)}")

