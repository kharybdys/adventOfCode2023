import re
from collections import defaultdict
from math import prod
from typing import Generator


NUMBER_PATTERN = re.compile(r"\d+")


def has_symbol(puzzle_input: list[str], min_x: int, min_y: int, max_x: int, max_y: int) -> tuple[str, int, int]:
    for y in range(max(0, min_y), min(len(puzzle_input), max_y+1)):
        line = puzzle_input[y]
        for x in range(max(0, min_x), min(len(line), max_x)):
            char = line[x]
            if not(char.isdigit() or char == "."):
                return char, x, y
    return "", 0, 0


def generate_part_numbers(puzzle_input: list[str]) -> Generator[int, None, None]:
    for y, line in enumerate(puzzle_input):
        for match in NUMBER_PATTERN.finditer(line):
            symbol, symb_x, symb_y = has_symbol(puzzle_input,
                                                min_x=match.start() - 1,
                                                min_y=y - 1,
                                                max_x=match.end() + 1,
                                                max_y=y + 1)
            if symbol:
                print(f"Number {match[0]} has an attaching symbol {symbol} at coordinates {symb_x}, {symb_y}")
                yield int(match[0])
            else:
                print(f"Number {match[0]} is not a part number at line {line}")


def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    solution = sum(generate_part_numbers(puzzle_input))
    print(solution)


def has_gear(puzzle_input: list[str], min_x: int, min_y: int, max_x: int, max_y: int) -> tuple[str, int, int]:
    for y in range(max(0, min_y), min(len(puzzle_input), max_y+1)):
        line = puzzle_input[y]
        for x in range(max(0, min_x), min(len(line), max_x)):
            char = line[x]
            if char == "*":
                return char, x, y
    return "", 0, 0


def generate_gear_numbers(puzzle_input: list[str]) -> Generator[tuple[int, int, int], None, None]:
    for y, line in enumerate(puzzle_input):
        for match in NUMBER_PATTERN.finditer(line):
            symbol, symb_x, symb_y = has_gear(puzzle_input,
                                              min_x=match.start() - 1,
                                              min_y=y - 1,
                                              max_x=match.end() + 1,
                                              max_y=y + 1)
            if symbol:
                yield int(match[0]), symb_x, symb_y


def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    gears_by_coords: dict[tuple[int, int], list[int]] = defaultdict(list)
    for gear, x, y in generate_gear_numbers(puzzle_input):
        gears_by_coords[(x,y)].append(gear)

    solution = sum(prod(gears) for gears in gears_by_coords.values() if len(gears) == 2)
    print(solution)
