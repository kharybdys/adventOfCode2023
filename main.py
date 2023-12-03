from argparse import ArgumentParser
from pathlib import Path
import re

import puzzle1a
import puzzle1b
import puzzle2
import puzzle2022_25
import puzzle3
import puzzle4

SOLVERS = {"1a": puzzle1a.solve,
           "1b": puzzle1b.solve,
           "2a": puzzle2.solve_a,
           "2b": puzzle2.solve_b,
           "3a": puzzle3.solve_a,
           "3b": puzzle3.solve_b,
           "4a": puzzle4.solve_a,
           "4b": puzzle4.solve_b,
           "2022_25a": puzzle2022_25.solve_a,
           "2022_25b": puzzle2022_25.solve_b,
           }

# I intend to manually change this for every puzzle
DEFAULT_PUZZLE = "3a"

PUZZLE_NUMBER_PATTERN = re.compile(r"[\d_]+")


def load_input(puzzle: str) -> list[str]:
    data_dir = Path(__file__).parent / "data"
    puzzle_number = PUZZLE_NUMBER_PATTERN.match(puzzle)[0]

    with open(data_dir / f"input{puzzle_number}.txt", "rt") as file:
        return [line.rstrip() for line in file]


if __name__ == "__main__":
    parser = ArgumentParser(prog="AdventOfCode2023_solver")
    parser.add_argument("-p", "--puzzle", default=DEFAULT_PUZZLE)
    args = parser.parse_args()
    if args.puzzle in SOLVERS:
        SOLVERS[args.puzzle](load_input(args.puzzle))
    else:
        raise NotImplementedError(f"No support for puzzle {args.puzzle}")

