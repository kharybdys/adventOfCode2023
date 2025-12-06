import sys
from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from functools import cache, cached_property

from registry import register_solver
from utils import Grid, PrintEnum, Direction, Coords


class TileStatus(PrintEnum):
    V_0 = "0", "0"
    V_1 = "1", "1"
    V_2 = "2", "2"
    V_3 = "3", "3"
    V_4 = "4", "4"
    V_5 = "5", "5"
    V_6 = "6", "6"
    V_7 = "7", "7"
    V_8 = "8", "8"
    V_9 = "9", "9"
    APPLY = "APPLY", "A"
    WALL = "WALL", "#"


TileGrid = Grid[TileStatus]


class Apply:
    str_repr = "A"


DirectionalKey = Direction | type[Apply]


EXPANSION_MAPPING: dict[tuple[DirectionalKey, ...], list[tuple[DirectionalKey, ...]]] = {
    (Apply, Apply): [(Apply,)],
    (Apply, Direction.SOUTH): [(Direction.SOUTH, Direction.WEST, Apply), (Direction.WEST, Direction.SOUTH, Apply)],
    (Apply, Direction.EAST): [(Direction.SOUTH, Apply), (Direction.WEST, Direction.SOUTH, Direction.EAST, Apply)],
    (Apply, Direction.NORTH): [(Direction.WEST, Apply), (Direction.SOUTH, Direction.WEST, Direction.NORTH, Apply)],
    (Apply, Direction.WEST): [(Direction.SOUTH, Direction.WEST, Direction.WEST, Apply), (Direction.WEST, Direction.SOUTH, Direction.WEST, Apply)],
    (Direction.SOUTH, Apply): [(Direction.NORTH, Direction.EAST, Apply), (Direction.EAST, Direction.NORTH, Apply)],
    (Direction.EAST, Apply): [(Direction.NORTH, Apply), (Direction.WEST, Direction.NORTH, Direction.EAST, Apply)],
    (Direction.NORTH, Apply): [(Direction.EAST, Apply), (Direction.SOUTH, Direction.EAST, Direction.NORTH, Apply)],
    (Direction.WEST, Apply): [(Direction.EAST, Direction.NORTH, Direction.EAST, Apply), (Direction.EAST, Direction.EAST, Direction.NORTH, Apply)],
    (Direction.SOUTH, Direction.SOUTH): [(Apply,)],
    (Direction.SOUTH, Direction.EAST): [(Direction.EAST, Apply), (Direction.NORTH, Direction.EAST, Direction.SOUTH, Apply)],
    (Direction.SOUTH, Direction.NORTH): [(Direction.NORTH, Apply), (Direction.EAST, Direction.NORTH, Direction.WEST, Apply)],
    (Direction.SOUTH, Direction.WEST): [(Direction.WEST, Apply)],
    (Direction.EAST, Direction.SOUTH): [(Direction.WEST, Apply), (Direction.NORTH, Direction.WEST, Direction.SOUTH, Apply)],
    (Direction.EAST, Direction.EAST): [(Apply,)],
    (Direction.EAST, Direction.NORTH): [(Direction.NORTH, Direction.WEST, Apply), (Direction.WEST, Direction.NORTH, Apply)],
    (Direction.EAST, Direction.WEST): [(Direction.WEST, Direction.WEST, Apply), (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.WEST, Apply)],
    (Direction.NORTH, Direction.SOUTH): [(Direction.SOUTH, Apply), (Direction.EAST, Direction.SOUTH, Direction.WEST, Apply)],
    (Direction.NORTH, Direction.EAST): [(Direction.EAST, Direction.SOUTH, Apply), (Direction.SOUTH, Direction.EAST, Apply)],
    (Direction.NORTH, Direction.NORTH): [(Apply,)],
    (Direction.NORTH, Direction.WEST): [(Direction.SOUTH, Direction.WEST, Apply), (Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.WEST, Apply)],
    (Direction.WEST, Direction.SOUTH): [(Direction.EAST, Apply)],
    (Direction.WEST, Direction.EAST): [(Direction.EAST, Direction.EAST, Apply), (Direction.EAST, Direction.NORTH, Direction.EAST, Direction.SOUTH, Apply)],
    (Direction.WEST, Direction.NORTH): [(Direction.EAST, Direction.NORTH, Apply), (Direction.EAST, Direction.EAST, Direction.NORTH, Direction.WEST, Apply)],
    (Direction.WEST, Direction.WEST): [(Apply,)],
}


def expand(instructions: tuple[DirectionalKey, ...]) -> Generator[tuple[DirectionalKey, ...], None, None]:
    if instructions in EXPANSION_MAPPING:
        for expansion in EXPANSION_MAPPING[instructions]:
            yield expansion
    elif len(instructions) < 2:
        raise ValueError("Should only need to recurse on a list of length at least 2")
    else:
        result = []
        for rest in expand(instructions[:-1]):
            for expansion in EXPANSION_MAPPING[instructions[-2], instructions[-1]]:
                result.append(rest + expansion)
        EXPANSION_MAPPING[instructions] = result
        # print(f"Updated mapping to # variations {len(result)} for {instructions}")
        yield from result


"""
v<<A  = <
>>^A  = A
<A    = ^
>A    = A
vA    = >
<^A   = ^
A     = ^
>A    = A
<vA   = v
A     = v
A     = v
>^A   = A

v<<A>>^A = <A    8 -> 2 
<A>A     = ^A    4 -> 2
vA<^AA>A = >^^A  8 -> 4
<vAAA>^A = vvvA  8 -> 4

"""


def split_instructions(instructions: tuple[DirectionalKey, ...]) -> Generator[tuple[DirectionalKey, ...], None, None]:
    previous_index = -1
    if instructions[-1] == Apply:
        for index in range(len(instructions)):
            if instructions[index] == Apply:
                yield instructions[previous_index + 1:index + 1]
                previous_index = index
    else:
        raise ValueError(f"Invalid instruction set, should always end with Apply, got {instructions}")


@cache
def calculate_instruction_length(instructions: tuple[DirectionalKey, ...], expansion_depth: int) -> int:
    if expansion_depth > 0:
        result = sys.maxsize
        for expansion in expand((Apply,) + instructions):
            expansion_length = 0
            for instruction in split_instructions(expansion):
                expansion_length += calculate_instruction_length(instructions=instruction,
                                                                 expansion_depth=expansion_depth - 1,
                                                                 )
            result = min(result, expansion_length)
        return result
    else:
        return len(instructions)


@dataclass
class PathAttempt:
    coords: Coords
    instructions: list[DirectionalKey]
    coords_visited: set[Coords]
    expansion_depth: int

    @cached_property
    def instruction_length(self) -> int:
        print(f"Calculating instruction length for {self.instructions}")
        return calculate_instruction_length(
            instructions=tuple(self.instructions),
            expansion_depth=self.expansion_depth,
        )


@cache
def find_smallest_path(keypad: TileGrid, from_tile: TileStatus, to_tile: TileStatus, expansion_depth: int) -> int:
    smallest_path: PathAttempt | None = None
    start_coords = list(keypad.all_coords_for({from_tile}))
    if len(start_coords) != 1:
        raise ValueError(f"Invalid keypad, need unique coords for {from_tile}")
    start_coords = Coords(*start_coords[0])
    boundary: deque[PathAttempt] = deque()
    boundary.append(
        PathAttempt(
            coords=start_coords,
            instructions=[],
            coords_visited={start_coords},
            expansion_depth=expansion_depth
        )
    )
    while boundary:
        path = boundary.pop()
        if keypad.value_at_or(*path.coords, default=TileStatus.WALL) == to_tile:
            path.instructions = path.instructions + [Apply]
            if smallest_path is None or path.instruction_length < smallest_path.instruction_length:
                smallest_path = path
        else:
            for direction in Direction.all():
                new_coords = Coords(*direction.next_coords(*path.coords))
                if new_coords not in path.coords_visited and keypad.value_at_or(*new_coords, default=TileStatus.WALL) != TileStatus.WALL:
                    new_path = PathAttempt(
                        coords=new_coords,
                        instructions=path.instructions + [direction],
                        coords_visited=path.coords_visited.union({new_coords}),
                        expansion_depth=expansion_depth,
                    )
                    boundary.append(new_path)
    print(f"Returning for {from_tile=}, {to_tile=}, {smallest_path.instruction_length=}")
    return smallest_path.instruction_length


def solve_numerical_keypad(keypad: TileGrid, code: list[TileStatus], expansion_depth: int) -> int:
    return sum(
        find_smallest_path(
            keypad=keypad,
            from_tile=TileStatus.APPLY if index == 0 else code[index-1],
            to_tile=to_tile,
            expansion_depth=expansion_depth,
        ) for index, to_tile in enumerate(code)
    )


def parse_code(line: str) -> tuple[int, list[TileStatus]]:
    return int(line[:-1]), list(map(TileStatus.from_char, line))


def solve(puzzle_input: list[str], expansion_depth: int) -> int:
    keypad = Grid.from_lines(["789", "456", "123", "#0A"], TileStatus.from_char)
    solution = 0
    for line in puzzle_input:
        value, code = parse_code(line)
        smallest_path_length = solve_numerical_keypad(keypad, code, expansion_depth)
        print(f"{smallest_path_length=} for {code=}")
        solution += smallest_path_length * value
    return solution


@register_solver(year="2024", key="21", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)

    print(f"Solution is {solve(puzzle_input, 2)}")


@register_solver(year="2024", key="21", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)

    print(f"Solution is {solve(puzzle_input, 25)}")
