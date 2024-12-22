import sys
from collections.abc import Generator

from registry import register_solver
from utils import Grid, PrintEnum, Direction


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


EXPANSION_MAPPING: dict[tuple[DirectionalKey, DirectionalKey], list[list[DirectionalKey]]] = {
    (Apply, Apply): [[Apply]],
    (Apply, Direction.SOUTH): [[Direction.SOUTH, Direction.WEST, Apply], [Direction.WEST, Direction.SOUTH, Apply]],
    (Apply, Direction.EAST): [[Direction.SOUTH, Apply], [Direction.WEST, Direction.SOUTH, Direction.EAST, Apply]],
    (Apply, Direction.NORTH): [[Direction.WEST, Apply], [Direction.SOUTH, Direction.WEST, Direction.NORTH, Apply]],
    (Apply, Direction.WEST): [[Direction.SOUTH, Direction.WEST, Direction.WEST, Apply], [Direction.WEST, Direction.SOUTH, Direction.WEST, Apply]],
    (Direction.SOUTH, Apply): [[Direction.NORTH, Direction.EAST, Apply], [Direction.EAST, Direction.NORTH, Apply]],
    (Direction.EAST, Apply): [[Direction.NORTH, Apply], [Direction.WEST, Direction.NORTH, Direction.EAST, Apply]],
    (Direction.NORTH, Apply): [[Direction.EAST, Apply], [Direction.SOUTH, Direction.EAST, Direction.NORTH, Apply]],
    (Direction.WEST, Apply): [[Direction.EAST, Direction.NORTH, Direction.EAST, Apply], [Direction.EAST, Direction.EAST, Direction.NORTH, Apply]],
    (Direction.SOUTH, Direction.SOUTH): [[Apply]],
    (Direction.SOUTH, Direction.EAST): [[Direction.EAST, Apply], [Direction.NORTH, Direction.EAST, Direction.SOUTH, Apply]],
    (Direction.SOUTH, Direction.NORTH): [[Direction.NORTH, Apply], [Direction.EAST, Direction.NORTH, Direction.WEST, Apply]],
    (Direction.SOUTH, Direction.WEST): [[Direction.WEST, Apply]],
    (Direction.EAST, Direction.SOUTH): [[Direction.WEST, Apply], [Direction.NORTH, Direction.WEST, Direction.SOUTH, Apply]],
    (Direction.EAST, Direction.EAST): [[Apply]],
    (Direction.EAST, Direction.NORTH): [[Direction.NORTH, Direction.WEST, Apply], [Direction.WEST, Direction.NORTH, Apply]],
    (Direction.EAST, Direction.WEST): [[Direction.WEST, Direction.WEST, Apply], [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.WEST, Apply]],
    (Direction.NORTH, Direction.SOUTH): [[Direction.SOUTH, Apply], [Direction.EAST, Direction.SOUTH, Direction.WEST, Apply]],
    (Direction.NORTH, Direction.EAST): [[Direction.EAST, Direction.SOUTH, Apply], [Direction.SOUTH, Direction.EAST, Apply]],
    (Direction.NORTH, Direction.NORTH): [[Apply]],
    (Direction.NORTH, Direction.WEST): [[Direction.SOUTH, Direction.WEST, Apply], [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.WEST, Apply]],
    (Direction.WEST, Direction.SOUTH): [[Direction.EAST, Apply]],
    (Direction.WEST, Direction.EAST): [[Direction.EAST, Direction.EAST, Apply], [Direction.EAST, Direction.NORTH, Direction.EAST, Direction.SOUTH, Apply]],
    (Direction.WEST, Direction.NORTH): [[Direction.EAST, Direction.NORTH, Apply], [Direction.EAST, Direction.EAST, Direction.NORTH, Direction.WEST, Apply]],
    (Direction.WEST, Direction.WEST): [[Apply]],
}


def expand(instructions: list[DirectionalKey], cut_off_length: int) -> Generator[list[DirectionalKey], None, None]:
    if len(instructions) == 1:
        yield from EXPANSION_MAPPING[Apply, instructions[0]]
    elif len(instructions) < 1:
        raise ValueError("Can only be executed on a list of length at least 1")
    else:
        for rest in expand(instructions[:-1], cut_off_length):
            for expansion in EXPANSION_MAPPING[instructions[-2], instructions[-1]]:
                if len(expansion) + len(rest) < cut_off_length:
                    yield expansion + rest


def parse_char(char: str) -> DirectionalKey:
    if char == "A":
        return Apply
    else:
        return Direction.from_char(char).opposite


def apply_expansions(cut_off_length: int, instructions: list[DirectionalKey]) -> Generator[list[DirectionalKey], None, None]:
    # instructions is the instructions for the robot on the numerical keypad
    for expansion_1 in expand(instructions, cut_off_length):
        # expansion_1 is the instructions for the robot in the high radiation area
        for expansion_2 in expand(expansion_1, cut_off_length):
            # expansion_2 is the isntructions for the robot in the freezing area
            for expansion_3 in expand(expansion_2, cut_off_length):
                # expansion_3 is finally what the solution will be.
                # Update the cut_off_length to save as much calculation time as possible
                cut_off_length = len(expansion_3)
                yield expansion_3


def solve_numerical_keypad(keypad: TileGrid, code: list[TileStatus]) -> int:
    min_solution_length = sys.maxsize
    # TODO: Solve this
    return min_solution_length


def parse_code(line: str) -> tuple[int, list[TileStatus]]:
    return int(line[:-1]), list(map(TileStatus.from_char, line))


@register_solver(year="2024", key="21", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)

    keypad = Grid.from_lines(["789", "456", "123", "#0A"], TileStatus.from_char)
    solution = 0
    for line in puzzle_input:
        value, code = parse_code(line)
        solution += solve_numerical_keypad(keypad, code) * value

    print(f"Solution is {solution}")


@register_solver(year="2024", key="21", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    print(f"Solution is TBD")
