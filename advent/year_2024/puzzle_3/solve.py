import re
from collections.abc import Generator
from itertools import chain, starmap

from registry import register_solver

SIMPLE_PATTERN = re.compile(r"mul\((\d+)\s*,\s*(\d+)\)")
DO_PATTERN_STRING = r"(?P<do>do\(\))"
DONT_PATTERN_STRING = r"(?P<dont>don't\(\))"
MUL_PATTERN_STRING = r"mul\((?P<mul1>\d+)\s*,\s*(?P<mul2>\d+)\)"
COMBINED_PATTERN = re.compile(DO_PATTERN_STRING + r"|" + DONT_PATTERN_STRING + r"|" + MUL_PATTERN_STRING)


def parse_line_simple(line: str) -> list[tuple[int, int]]:
    return SIMPLE_PATTERN.findall(line)


def parse_line_complex(line: str) -> Generator[tuple[int], None, None]:
    do = True
    line_to_go = line
    while result := COMBINED_PATTERN.search(line_to_go):
        print(f"{result}, {result.groupdict()}")
        if result.group("do"):
            if not do:
                print("Enabling processing")
            do = True
        elif result.group("dont"):
            if do:
                print("Stopping processing")
            do = False
        elif result.group("mul1"):
            if do:
                mul = multiply(result.group("mul1"), result.group("mul2"))
                print(f"Yielding {mul}")
                yield mul
        line_to_go = line_to_go[result.end():]


def multiply(a: str, b: str) -> int:
    return int(a) * int(b)


@register_solver(year="2024", key="3", variation="a")
def solve_a(puzzle_input: list[str], example: bool) -> None:
    solution = sum(starmap(multiply, chain(*map(parse_line_simple, puzzle_input))))
    print(f"Solution is {solution}")


@register_solver(year="2024", key="3", variation="b")
def solve_b(puzzle_input: list[str], example: bool) -> None:
    solution = sum(parse_line_complex("".join(puzzle_input)))
    print(f"Solution is {solution}")
