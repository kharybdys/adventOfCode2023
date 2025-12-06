from argparse import ArgumentParser
from pathlib import Path

from advent.registry import get_solver, import_all_solvers


def load_input(year: str, key: str, example: bool) -> list[str]:
    data_dir = Path(__file__).parent.parent / "data"

    example_postfix = "_example" if example else ""
    with open(data_dir / year / f"input{key}{example_postfix}.txt", "rt") as file:
        return [line.rstrip() for line in file]


def main():
    import_all_solvers()

    parser = ArgumentParser(prog="AdventOfCode_solver")
    parser.add_argument("-y", "--year", required=True)
    parser.add_argument("-p", "--puzzle", required=True)
    parser.add_argument("-v", "--variation", required=True)
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()
    solver = get_solver(year=args.year, key=args.puzzle, variation=args.variation)
    if solver:
        puzzle_input = load_input(year=args.year, key=args.puzzle, example=args.example)
        solver(puzzle_input=puzzle_input, example=args.example)
    else:
        raise NotImplementedError(f"No support for combination {args.year}, {args.puzzle}, {args.variation}")


if __name__ == "__main__":
    main()
