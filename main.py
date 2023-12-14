from argparse import ArgumentParser
from pathlib import Path
import re

import puzzle10
import puzzle11
import puzzle12
import puzzle13
import puzzle14
import puzzle15
import puzzle1a
import puzzle1b
import puzzle2
import puzzle2021_24
import puzzle2021_25
import puzzle2022_11
import puzzle2022_25
import puzzle3
import puzzle4
import puzzle5
import puzzle6
import puzzle7
import puzzle8
import puzzle9

SOLVERS = {"1a": puzzle1a.solve,
           "1b": puzzle1b.solve,
           "2a": puzzle2.solve_a,
           "2b": puzzle2.solve_b,
           "3a": puzzle3.solve_a,
           "3b": puzzle3.solve_b,
           "4a": puzzle4.solve_a,
           "4b": puzzle4.solve_b,
           "5a": puzzle5.solve_a,
           "5b": puzzle5.solve_b,
           "6a": puzzle6.solve_a,
           "6b": puzzle6.solve_b,
           "7a": puzzle7.solve_a,
           "7b": puzzle7.solve_b,
           "8a": puzzle8.solve_a,
           "8b": puzzle8.solve_b,
           "9a": puzzle9.solve_a,
           "9b": puzzle9.solve_b,
           "10a": puzzle10.solve_a,
           "10b": puzzle10.solve_b,
           "11a": puzzle11.solve_a,
           "11b": puzzle11.solve_b,
           "12a": puzzle12.solve_a,
           "12b": puzzle12.solve_b,
           "13a": puzzle13.solve_a,
           "13b": puzzle13.solve_b,
           "14a": puzzle14.solve_a,
           "14b": puzzle14.solve_b,
           "15a": puzzle15.solve_a,
           "15b": puzzle15.solve_b,
           "2021_24a": puzzle2021_24.solver.solve_a_too_slow,
           "2021_24b": puzzle2021_24.solve_b,
           "2021_25a": puzzle2021_25.solve_a,
           "2021_25b": puzzle2021_25.solve_b,
           "2022_11a": puzzle2022_11.solve_a,
           "2022_11b": puzzle2022_11.solve_b,
           "2022_25a": puzzle2022_25.solve_a,
           "2022_25b": puzzle2022_25.solve_b,
           }

# I intend to manually change this for every puzzle
DEFAULT_PUZZLE = "13b"
EXAMPLE = False

PUZZLE_NUMBER_PATTERN = re.compile(r"[\d_]+")


def load_input(puzzle: str) -> list[str]:
    data_dir = Path(__file__).parent / "data"
    puzzle_number = PUZZLE_NUMBER_PATTERN.match(puzzle)[0]

    example_postfix = "_example" if EXAMPLE else ""
    with open(data_dir / f"input{puzzle_number}{example_postfix}.txt", "rt") as file:
        return [line.rstrip() for line in file]


if __name__ == "__main__":
    parser = ArgumentParser(prog="AdventOfCode2023_solver")
    parser.add_argument("-p", "--puzzle", default=DEFAULT_PUZZLE)
    args = parser.parse_args()
    if args.puzzle in SOLVERS:
        SOLVERS[args.puzzle](load_input(args.puzzle))
    else:
        raise NotImplementedError(f"No support for puzzle {args.puzzle}")

