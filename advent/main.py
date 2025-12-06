from argparse import ArgumentParser
from pathlib import Path

from advent.registry import get_solver, import_all_solvers

# I intend to manually change this for every puzzle
DEFAULT_YEAR = "2025"
DEFAULT_PUZZLE = "1"
DEFAULT_VARIATION = "a"
EXAMPLE = False


def load_input(year: str, key: str) -> list[str]:
    data_dir = Path(__file__).parent.parent / "data"

    example_postfix = "_example" if EXAMPLE else ""
    with open(data_dir / year / f"input{key}{example_postfix}.txt", "rt") as file:
        return [line.rstrip() for line in file]


def main():
    import_all_solvers()

    parser = ArgumentParser(prog="AdventOfCode_solver")
    parser.add_argument("-y", "--year", default=DEFAULT_YEAR)
    parser.add_argument("-p", "--puzzle", default=DEFAULT_PUZZLE)
    parser.add_argument("-v", "--variation", default=DEFAULT_VARIATION)
    args = parser.parse_args()
    solver = get_solver(year=args.year, key=args.puzzle, variation=args.variation)
    if solver:
        puzzle_input = load_input(year=args.year, key=args.puzzle)
        solver(puzzle_input=puzzle_input, example=EXAMPLE)
    else:
        raise NotImplementedError(f"No support for combination {args.year}, {args.puzzle}, {args.variation}")


if __name__ == "__main__":
    main()
