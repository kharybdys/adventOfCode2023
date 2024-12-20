import re
from collections import deque, defaultdict
from dataclasses import dataclass
from itertools import batched
from typing import Generator

from registry import register_solver
from utils import Direction, Grid, Coords, Range

DEBUG = False

BoolGrid = Grid[bool]


@dataclass(repr=True)
class DigInstruction:
    direction: Direction
    distance: int
    hex: str

    def parse_hex(self):
        self.distance = int(self.hex[:5], 16)
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


# Initial solution for Part One. Too naive for Part Two
def solve_dig_instructions(dig_instructions: list[DigInstruction], print_grid: bool = True) -> int:
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
    if print_grid:
        grid.print_grid(lambda t: "#" if t else ".")
    fill_grid(grid, *find_inside_start(grid))
    if print_grid:
        print("Final filled grid: ")
        grid.print_grid(lambda t: "#" if t else ".")
    return sum(1 for tile in grid.tiles_iterator if tile)


def find_duplicated_dig_instruction(dig_instructions: list[DigInstruction]) -> bool:
    for i in range(0, len(dig_instructions)):
        curr = dig_instructions[i - 1]
        nxt = dig_instructions[i]
        if curr.direction == nxt.direction:
            curr.distance += nxt.distance
            dig_instructions.remove(nxt)
            return True
    return False


def solve_dig_instructions_for_big_numbers(dig_instructions: list[DigInstruction]) -> int:
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    negative_correction = 0
    current_x, current_y = 0, 0
    for dig_instruction in dig_instructions:
        new_x, new_y = dig_instruction.direction.next_coords(current_x, current_y, steps=dig_instruction.distance)
        if new_x > max_x:
            pass
        elif new_x < min_x:
            pass
        elif new_y > max_y:
            pass
        elif new_y < min_y:
            pass

    confirmed_dug = 0
    count_dig_instructions = len(dig_instructions) + 1
    while dig_instructions:
        if len(dig_instructions) == count_dig_instructions:
            print(f"Progress is stuck, confirmed_dug = {confirmed_dug}")
            simple_grid_solution = solve_dig_instructions(dig_instructions, print_grid=False)
            print(simple_grid_solution)
            return confirmed_dug + simple_grid_solution
        count_dig_instructions = len(dig_instructions)
        while find_duplicated_dig_instruction(dig_instructions):
            pass
        if DEBUG:
            for dig_instruction in dig_instructions:
                print(dig_instruction)
        else:
            print(f"Length of dig_instructions reduced to: {len(dig_instructions)}")
        if dig_instructions:
            if DEBUG:
                print(f"Next iteration, {confirmed_dug=}: ")
            for i in range(0, len(dig_instructions)):
                prev = dig_instructions[i - 2]
                curr = dig_instructions[i - 1]
                nxt = dig_instructions[i]
                if prev.direction.opposite == nxt.direction and curr.direction == prev.direction.cw:
                    if DEBUG:
                        print(f"Found bulge, {prev=}, {curr=}, {nxt=}")
                    if prev.distance < nxt.distance:
                        if DEBUG:
                            print(f"Removing {prev}")
                        dig_instructions.remove(prev)
                        w = prev.distance
                        nxt.distance -= prev.distance
                    elif prev.distance == nxt.distance:
                        if DEBUG:
                            print(f"Removing {nxt}")
                            print(f"Removing {prev}")
                        dig_instructions.remove(nxt)
                        dig_instructions.remove(prev)
                        w = prev.distance
                    elif nxt.distance <= prev.distance:
                        if DEBUG:
                            print(f"Removing {nxt}")
                        dig_instructions.remove(nxt)
                        prev.distance -= nxt.distance
                        w = nxt.distance
                    else:
                        raise ValueError("Unreachable")
                    confirmed_dug += (curr.distance + 1) * w
                    break
                if curr.direction.opposite == nxt.direction:
                    if DEBUG:
                        print(f"Found opposite directions, {curr=}, {nxt=}")
                    if curr.distance > nxt.distance:
                        curr.distance -= nxt.distance
                        if DEBUG:
                            print(f"Removing {nxt}")
                        dig_instructions.remove(nxt)
                        w = nxt.distance
                    elif curr.distance == nxt.distance:
                        if DEBUG:
                            print(f"Removing {nxt}")
                            print(f"Removing {curr}")
                        dig_instructions.remove(nxt)
                        dig_instructions.remove(curr)
                        w = nxt.distance
                    elif curr.distance < nxt.distance:
                        nxt.distance -= curr.distance
                        if DEBUG:
                            print(f"Removing {curr}")
                        dig_instructions.remove(curr)
                        w = curr.distance
                    else:
                        raise ValueError("Unreachable")
                    confirmed_dug += w
                    break

    print(dig_instructions)
    return confirmed_dug + 1  # Correct for final untracked square (the one we end up after reduction)


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


def calculate_area_by_vertices_and_slicing(dig_instructions: list[DigInstruction]) -> int:
    coords = Coords(0, 0)
    edges: set[Coords] = {coords}
    for dig_instruction in dig_instructions:
        print(f"{dig_instruction=}")
        coords = Coords(*dig_instruction.direction.next_coords(*coords, steps=dig_instruction.distance))
        print(f"{coords.x:10}, {coords.y:10}")
        edges.add(coords)
    if coords == Coords(0, 0):
        pass
    elif coords.x == 0 or coords.y == 0:
        edges.remove(coords)
    else:
        raise ValueError(f"Should end at one of the axis (preferably at origin), but ended up at {coords}")

    edges_by_x: dict[int, set[Coords]] = defaultdict(set)
    for edge in sorted(edges):
        edges_by_x[edge.x].add(edge)

    dig = 0
    while len(edges_by_x.keys()) > 2:
        x = min(edges_by_x.keys())
        next_x = min(e_x for e_x in edges_by_x.keys() if e_x != x)
        print(f"     {sorted(edges_by_x[x])=}")
        print(f"{sorted(edges_by_x[next_x])=}")
        print(f"                       {dig=}")
        if len(edges_by_x[x]) % 2 != 0:
            raise ValueError(f"Should have an even number of coordinates on each x, not so: {edges_by_x[x]}")
        for start_edge, end_edge in batched(sorted(edges_by_x[x]), 2):
            dig += (end_edge.y - start_edge.y + 1) * (next_x - x)

            next_start_edge = Coords(next_x, start_edge.y)
            if next_start_edge in edges_by_x[next_x]:
                edges_by_x[next_x].remove(next_start_edge)
            else:
                edges_by_x[next_x].add(next_start_edge)

            next_end_edge = Coords(next_x, end_edge.y)
            if next_end_edge in edges_by_x[next_x]:
                edges_by_x[next_x].remove(next_end_edge)
            else:
                edges_by_x[next_x].add(next_end_edge)

            next_ys = list(sorted(edge.y for edge in edges_by_x[next_x]))

            for start_y, end_y in batched(next_ys[1:-1], 2):
                if start_y > start_edge.y and end_y < end_edge.y:
                    dig += end_y - start_y - 1

        del edges_by_x[x]
    print(f"{dig=}")
    print(f"{edges_by_x=}")
    if any(len(ys) % 2 != 0 for ys in edges_by_x.values()):
        raise ValueError("Invalid end situation, should have exactly an even amount of values that form one or more rectangles")
    x = min(edges_by_x.keys())
    next_x = min(e_x for e_x in edges_by_x.keys() if e_x != x)
    ys = {c.y for edges in edges_by_x.values() for c in edges}
    if any(len(ys) != len(vs) for vs in edges_by_x.values()):
        raise ValueError("Remaining two columns coordinates do not have equal y values")
    for start_y, end_y in batched(sorted(ys), 2):
        dig += (next_x - x + 1) * (end_y - start_y + 1)
        print(f"{dig=} after {next_x=}, {x=}, {end_y=}, {start_y=}")

    return dig


@register_solver(year="2023", key="18", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    dig_instructions = list(parse(puzzle_input))
    print(calculate_area_by_vertices_and_slicing(dig_instructions))


def solve_b_naive(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    dig_instructions = list(parse(puzzle_input))
    for dig_instruction in dig_instructions:
        dig_instruction.parse_hex()
    print(solve_dig_instructions_for_big_numbers(dig_instructions))


# Latest idea: Bulges but as negative bulges, ie expand the grid to something rectangular and keep track what I needed to add
def solve_b_negative_bulges(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    dig_instructions = list(parse(puzzle_input))
    for dig_instruction in dig_instructions:
        dig_instruction.parse_hex()
        print(dig_instruction)
    print(solve_dig_instructions_for_big_numbers(dig_instructions))


@register_solver(year="2023", key="18", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    dig_instructions = list(parse(puzzle_input))
    for dig_instruction in dig_instructions:
        dig_instruction.parse_hex()
    print(calculate_area_by_vertices_and_slicing(dig_instructions))
