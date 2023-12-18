import re
from collections import deque
from dataclasses import dataclass
from typing import Generator

from utils import Direction, Grid


BoolGrid = Grid[bool]


@dataclass(repr=True)
class DigInstruction:
    direction: Direction
    distance: int
    hex: str

    def parse_hex(self):
        self.distance = int(self.hex[:4], 16)
        match self.hex[5]:
            case "0":
                self.direction = Direction.EAST
            case "1":
                self.direction = Direction.SOUTH
            case "2":
                self.direction = Direction.WEST
            case "3":
                self.direction = Direction.NORTH
            case _:
                raise ValueError("Invalid hex value for a dig instruction")


def analyze(dig_instructions: list[DigInstruction]) -> tuple[int, int, int, int]:
    # If we start at 0, 0, what are the min_x, max_x, min_y and max_y
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    current_x, current_y = 0, 0
    for dig_instruction in dig_instructions:
        current_x, current_y = dig_instruction.direction.next_coords(current_x, current_y, dig_instruction.distance)
        min_x = min(min_x, current_x)
        max_x = max(max_x, current_x)
        min_y = min(min_y, current_y)
        max_y = max(max_y, current_y)
    return max_x - min_x + 1, max_y - min_y + 1, -min_x, -min_y


def find_inside_start(grid: BoolGrid) -> tuple[int, int]:
    # Find the empty entry on line 1 that has a filled entry on line 0:
    for x in range(0, grid.width):
        if not grid.value_at(x, 1) and grid.value_at(x, 0):
            return x, 1


def fill_grid(grid: BoolGrid, start_x, start_y):
    fills = 0
    frontier = deque()
    frontier.append((start_x, start_y))
    while frontier:
        x, y = frontier.popleft()
        if not grid.value_at(x, y):
            grid.set_value_at(x, y, True)
            fills += 1
            for direction in Direction.all():
                new_x, new_y = direction.next_coords(x, y)
                if grid.within_bounds(new_x, new_y) and not grid.value_at(new_x, new_y):
                    frontier.append((new_x, new_y))


def solve_dig_instructions(dig_instructions: list[DigInstruction]) -> int:
    width, height, start_x, start_y = analyze(dig_instructions)
    print(f"{width=}, {height=}, {start_x=}, {start_y=}")
    grid: BoolGrid = Grid([[False for _ in range(0, width)] for _ in range(0, height)])
    x, y = start_x, start_y
    for dig_instruction in dig_instructions:
        print(f"Processing {dig_instruction=}")
        for _ in range(0, dig_instruction.distance):
            if grid.within_bounds(x, y):
                grid.set_value_at(x, y, True)
                x, y = dig_instruction.direction.next_coords(x, y)
            else:
                raise ValueError(f"Invalid coordinates {x}, {y} for grid with width {grid.width} and height {grid.height}")
    grid.print_grid(lambda t: "#" if t else ".")
    fill_grid(grid, *find_inside_start(grid))
    print("Final filled grid: ")
    grid.print_grid(lambda t: "#" if t else ".")
    return sum(1 for tile in grid.tiles_iterator if tile)


def parse(puzzle_input: list[str]) -> Generator[DigInstruction, None, None]:
    INPUT_PATTERN = re.compile(r"(U|D|L|R) (\d+) \(#([a-f0-9]{6})\)")
    direction_map = {"U": Direction.NORTH,
                     "R": Direction.EAST,
                     "D": Direction.SOUTH,
                     "L": Direction.WEST}
    for line in puzzle_input:
        if match := INPUT_PATTERN.fullmatch(line):
            direction = direction_map[match[1]]
            hex = match[3]
            yield DigInstruction(direction=direction, distance=int(match[2]), hex=hex)
        else:
            raise ValueError(f"Invalid line {line}")


def solve_a(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    dig_instructions = list(parse(puzzle_input))
    print(solve_dig_instructions(dig_instructions))


def solve_b(puzzle_input: list[str]) -> None:
    print(puzzle_input)
    dig_instructions = list(parse(puzzle_input))
    for dig_instruction in dig_instructions:
        dig_instruction.parse_hex()
    print(solve_dig_instructions(dig_instructions))
