import re

from pathlib import Path
from typing import Generator

from advent.earlier_years.puzzle2021_25.sea_floor import SeaFloor
from registry import register_solver


def read_expected_output_for_example() -> Generator[tuple[int, SeaFloor], None, None]:
    START_LINE_PATTERN = re.compile(r"After (\d+) steps?:")
    puzzle_input = []
    step = 0
    with open(Path(__file__).parent / "expected_output.txt", "rt") as file:
        for line in file:
            line = line.rstrip()
            if line:
                if match := START_LINE_PATTERN.fullmatch(line):
                    if puzzle_input:
                        yield step, SeaFloor.parse(puzzle_input)
                        puzzle_input = []
                    step = int(match[1])
                else:
                    puzzle_input.append(line)


@register_solver(year="2021", key="25", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    moved = True
    steps = 0
    sea_floor = SeaFloor.parse(puzzle_input)
    sea_floor.print()

    expected_output_for_example = {step: floor for step, floor in read_expected_output_for_example()} if example else {}
    print(expected_output_for_example)
    while moved:
        moved = sea_floor.move()
        steps += 1
        print("")
        print(f"At step {steps}, {moved=}")
        sea_floor.print()

        if example and steps in expected_output_for_example:
            print(f"MMAARRTTEE: expected_output_for_example matches: {expected_output_for_example[steps] == sea_floor}")
    print("")
    print(f"Steps: {steps}")


@register_solver(year="2021", key="25", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    print(puzzle_input)
    print("No Part Two for day 25!")
