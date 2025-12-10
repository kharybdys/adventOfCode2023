from itertools import combinations

from advent.registry import register_solver
from advent.utils.grid import Coords


def parse_line(line: str) -> Coords:
    parts = line.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid line, expected two parts separated by comma: {line}")
    return Coords(x=int(parts[0]), y=int(parts[1]))


@register_solver(year="2025", key="9", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    coords = list(map(parse_line, puzzle_input))
    solution = 0
    for corner_1, corner_2 in combinations(coords, 2):
        size = abs((corner_1.x - corner_2.x) + 1) * abs((corner_1.y - corner_2.y) + 1)
        if size > solution:
            solution = size
    print(f"Solution is {solution}")


@register_solver(year="2025", key="9", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = 0
    print(f"Solution is {solution}")
