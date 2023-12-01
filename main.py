from argparse import ArgumentParser
from pathlib import Path

import puzzle1a
import puzzle1b
import puzzle2a
import puzzle2b

SOLVERS = {"1a": puzzle1a.solve,
           "1b": puzzle1b.solve,
           "2a": puzzle2a.solve,
           "2b": puzzle2b.solve}

# I intend to manually change this for every puzzle
DEFAULT_PUZZLE = "1a"


def load_input(puzzle: str) -> list[str]:
    data_dir = Path(__file__).parent / "data"
    with open(data_dir / f"input{puzzle}.txt", "rt") as file:
        return [line.rstrip() for line in file]


if __name__ == "__main__":
    parser = ArgumentParser(prog="AdventOfCode2023_solver")
    parser.add_argument("-p", "--puzzle", default=DEFAULT_PUZZLE)
    args = parser.parse_args()
    if args.puzzle in SOLVERS:
        SOLVERS[args.puzzle](load_input(args.puzzle))
    else:
        raise NotImplementedError(f"No support for puzzle {args.puzzle}")

